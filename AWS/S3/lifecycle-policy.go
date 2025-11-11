package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/aws-sdk-go-v2/service/s3/types"
)

type LifecyclePolicyManager struct {
	client *s3.Client
	ctx    context.Context
}

func NewLifecyclePolicyManager(region string) (*LifecyclePolicyManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &LifecyclePolicyManager{
		client: s3.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *LifecyclePolicyManager) SetLifecyclePolicy(bucketName string) error {
	input := &s3.PutBucketLifecycleConfigurationInput{
		Bucket: &bucketName,
		LifecycleConfiguration: &types.BucketLifecycleConfiguration{
			Rules: []types.LifecycleRule{
				{
					Id:     strPtr("archive-old-objects"),
					Status: types.ExpirationStatusEnabled,
					Transitions: []types.Transition{
						{
							Days:         intPtr(30),
							StorageClass: types.TransitionStorageClassStandardIa,
						},
						{
							Days:         intPtr(90),
							StorageClass: types.TransitionStorageClassGlacier,
						},
					},
					Expiration: &types.LifecycleExpiration{
						Days: intPtr(365),
					},
				},
			},
		},
	}

	_, err := m.client.PutBucketLifecycleConfiguration(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to set lifecycle policy: %w", err)
	}

	log.Printf("Successfully set lifecycle policy for bucket: %s", bucketName)
	return nil
}

func strPtr(s string) *string { return &s }
func intPtr(i int32) *int32   { return &i }

func main() {
	manager, err := NewLifecyclePolicyManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.SetLifecyclePolicy("my-bucket")
	if err != nil {
		log.Fatal(err)
	}
}
