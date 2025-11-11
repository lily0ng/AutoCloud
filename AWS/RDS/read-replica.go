package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/rds"
)

type ReadReplicaManager struct {
	client *rds.Client
	ctx    context.Context
}

func NewReadReplicaManager(region string) (*ReadReplicaManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &ReadReplicaManager{
		client: rds.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *ReadReplicaManager) CreateReadReplica(sourceDBID, replicaID string) error {
	input := &rds.CreateDBInstanceReadReplicaInput{
		SourceDBInstanceIdentifier: &sourceDBID,
		DBInstanceIdentifier:       &replicaID,
		DBInstanceClass:            strPtr("db.t3.micro"),
		PubliclyAccessible:         boolPtr(false),
	}

	_, err := m.client.CreateDBInstanceReadReplica(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to create read replica: %w", err)
	}

	log.Printf("Successfully created read replica: %s", replicaID)
	return nil
}

func strPtr(s string) *string { return &s }
func boolPtr(b bool) *bool    { return &b }

func main() {
	manager, err := NewReadReplicaManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.CreateReadReplica("autocloud-db", "autocloud-db-replica")
	if err != nil {
		log.Fatal(err)
	}
}
