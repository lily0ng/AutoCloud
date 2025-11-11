package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
)

type AccessControlManager struct {
	client *s3.Client
	ctx    context.Context
}

func NewAccessControlManager(region string) (*AccessControlManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &AccessControlManager{
		client: s3.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *AccessControlManager) SetBucketPolicy(bucketName string) error {
	policy := map[string]interface{}{
		"Version": "2012-10-17",
		"Statement": []map[string]interface{}{
			{
				"Sid":    "PublicReadGetObject",
				"Effect": "Allow",
				"Principal": "*",
				"Action": "s3:GetObject",
				"Resource": fmt.Sprintf("arn:aws:s3:::%s/*", bucketName),
			},
		},
	}

	policyJSON, err := json.Marshal(policy)
	if err != nil {
		return fmt.Errorf("failed to marshal policy: %w", err)
	}

	policyStr := string(policyJSON)
	input := &s3.PutBucketPolicyInput{
		Bucket: &bucketName,
		Policy: &policyStr,
	}

	_, err = m.client.PutBucketPolicy(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to set bucket policy: %w", err)
	}

	log.Printf("Successfully set bucket policy for: %s", bucketName)
	return nil
}

func main() {
	manager, err := NewAccessControlManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.SetBucketPolicy("my-bucket")
	if err != nil {
		log.Fatal(err)
	}
}
