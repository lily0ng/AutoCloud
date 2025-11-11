package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/aws-sdk-go-v2/service/s3/types"
)

type VersioningManager struct {
	client *s3.Client
	ctx    context.Context
}

func NewVersioningManager(region string) (*VersioningManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &VersioningManager{
		client: s3.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *VersioningManager) EnableVersioning(bucketName string) error {
	input := &s3.PutBucketVersioningInput{
		Bucket: &bucketName,
		VersioningConfiguration: &types.VersioningConfiguration{
			Status: types.BucketVersioningStatusEnabled,
		},
	}

	_, err := m.client.PutBucketVersioning(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to enable versioning: %w", err)
	}

	log.Printf("Successfully enabled versioning for bucket: %s", bucketName)
	return nil
}

func (m *VersioningManager) SuspendVersioning(bucketName string) error {
	input := &s3.PutBucketVersioningInput{
		Bucket: &bucketName,
		VersioningConfiguration: &types.VersioningConfiguration{
			Status: types.BucketVersioningStatusSuspended,
		},
	}

	_, err := m.client.PutBucketVersioning(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to suspend versioning: %w", err)
	}

	log.Printf("Successfully suspended versioning for bucket: %s", bucketName)
	return nil
}

func main() {
	manager, err := NewVersioningManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.EnableVersioning("my-bucket")
	if err != nil {
		log.Fatal(err)
	}
}
