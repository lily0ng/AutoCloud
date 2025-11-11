package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/aws-sdk-go-v2/service/s3/types"
)

type ReplicationManager struct {
	client *s3.Client
	ctx    context.Context
}

func NewReplicationManager(region string) (*ReplicationManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &ReplicationManager{
		client: s3.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *ReplicationManager) SetupReplication(sourceBucket, destBucket, roleArn string) error {
	input := &s3.PutBucketReplicationInput{
		Bucket: &sourceBucket,
		ReplicationConfiguration: &types.ReplicationConfiguration{
			Role: &roleArn,
			Rules: []types.ReplicationRule{
				{
					ID:     strPtr("replicate-all"),
					Status: types.ReplicationRuleStatusEnabled,
					Priority: intPtr(1),
					Filter: &types.ReplicationRuleFilterMemberPrefix{
						Value: "",
					},
					Destination: &types.Destination{
						Bucket: strPtr(fmt.Sprintf("arn:aws:s3:::%s", destBucket)),
					},
				},
			},
		},
	}

	_, err := m.client.PutBucketReplication(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to setup replication: %w", err)
	}

	log.Printf("Successfully setup replication from %s to %s", sourceBucket, destBucket)
	return nil
}

func strPtr(s string) *string { return &s }
func intPtr(i int32) *int32   { return &i }

func main() {
	manager, err := NewReplicationManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.SetupReplication("source-bucket", "dest-bucket", "arn:aws:iam::123456789:role/replication-role")
	if err != nil {
		log.Fatal(err)
	}
}
