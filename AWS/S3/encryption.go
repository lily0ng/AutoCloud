package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/aws-sdk-go-v2/service/s3/types"
)

type EncryptionManager struct {
	client *s3.Client
	ctx    context.Context
}

func NewEncryptionManager(region string) (*EncryptionManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &EncryptionManager{
		client: s3.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *EncryptionManager) EnableEncryption(bucketName string) error {
	input := &s3.PutBucketEncryptionInput{
		Bucket: &bucketName,
		ServerSideEncryptionConfiguration: &types.ServerSideEncryptionConfiguration{
			Rules: []types.ServerSideEncryptionRule{
				{
					ApplyServerSideEncryptionByDefault: &types.ServerSideEncryptionByDefault{
						SSEAlgorithm: types.ServerSideEncryptionAes256,
					},
				},
			},
		},
	}

	_, err := m.client.PutBucketEncryption(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to enable encryption: %w", err)
	}

	log.Printf("Successfully enabled encryption for bucket: %s", bucketName)
	return nil
}

func main() {
	manager, err := NewEncryptionManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.EnableEncryption("my-bucket")
	if err != nil {
		log.Fatal(err)
	}
}
