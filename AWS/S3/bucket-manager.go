package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/aws-sdk-go-v2/service/s3/types"
)

type S3Manager struct {
	client *s3.Client
	ctx    context.Context
}

func NewS3Manager(region string) (*S3Manager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &S3Manager{
		client: s3.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *S3Manager) CreateBucket(bucketName string) error {
	_, err := m.client.CreateBucket(m.ctx, &s3.CreateBucketInput{
		Bucket: &bucketName,
		CreateBucketConfiguration: &types.CreateBucketConfiguration{
			LocationConstraint: types.BucketLocationConstraintUsEast1,
		},
	})
	if err != nil {
		return fmt.Errorf("failed to create bucket: %w", err)
	}

	log.Printf("Successfully created bucket: %s", bucketName)
	return nil
}

func (m *S3Manager) DeleteBucket(bucketName string) error {
	_, err := m.client.DeleteBucket(m.ctx, &s3.DeleteBucketInput{
		Bucket: &bucketName,
	})
	if err != nil {
		return fmt.Errorf("failed to delete bucket: %w", err)
	}

	log.Printf("Successfully deleted bucket: %s", bucketName)
	return nil
}

func (m *S3Manager) ListBuckets() ([]types.Bucket, error) {
	result, err := m.client.ListBuckets(m.ctx, &s3.ListBucketsInput{})
	if err != nil {
		return nil, fmt.Errorf("failed to list buckets: %w", err)
	}

	return result.Buckets, nil
}

func (m *S3Manager) EnableVersioning(bucketName string) error {
	_, err := m.client.PutBucketVersioning(m.ctx, &s3.PutBucketVersioningInput{
		Bucket: &bucketName,
		VersioningConfiguration: &types.VersioningConfiguration{
			Status: types.BucketVersioningStatusEnabled,
		},
	})
	if err != nil {
		return fmt.Errorf("failed to enable versioning: %w", err)
	}

	log.Printf("Successfully enabled versioning for bucket: %s", bucketName)
	return nil
}

func main() {
	manager, err := NewS3Manager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	buckets, err := manager.ListBuckets()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Found %d buckets\n", len(buckets))
}
