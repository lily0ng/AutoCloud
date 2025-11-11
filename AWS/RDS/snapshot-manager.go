package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/rds"
)

type SnapshotManager struct {
	client *rds.Client
	ctx    context.Context
}

func NewSnapshotManager(region string) (*SnapshotManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &SnapshotManager{
		client: rds.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *SnapshotManager) CreateSnapshot(dbInstanceID, snapshotID string) error {
	input := &rds.CreateDBSnapshotInput{
		DBInstanceIdentifier: &dbInstanceID,
		DBSnapshotIdentifier: &snapshotID,
	}

	_, err := m.client.CreateDBSnapshot(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to create snapshot: %w", err)
	}

	log.Printf("Successfully created snapshot: %s", snapshotID)
	return nil
}

func (m *SnapshotManager) RestoreFromSnapshot(snapshotID, newDBInstanceID string) error {
	input := &rds.RestoreDBInstanceFromDBSnapshotInput{
		DBSnapshotIdentifier: &snapshotID,
		DBInstanceIdentifier: &newDBInstanceID,
	}

	_, err := m.client.RestoreDBInstanceFromDBSnapshot(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to restore from snapshot: %w", err)
	}

	log.Printf("Successfully restored database from snapshot: %s", snapshotID)
	return nil
}

func main() {
	manager, err := NewSnapshotManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.CreateSnapshot("autocloud-db", "autocloud-snapshot-001")
	if err != nil {
		log.Fatal(err)
	}
}
