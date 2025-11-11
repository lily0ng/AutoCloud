package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/rds"
)

type MultiAZManager struct {
	client *rds.Client
	ctx    context.Context
}

func NewMultiAZManager(region string) (*MultiAZManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &MultiAZManager{
		client: rds.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *MultiAZManager) EnableMultiAZ(dbInstanceID string) error {
	input := &rds.ModifyDBInstanceInput{
		DBInstanceIdentifier: &dbInstanceID,
		MultiAZ:              boolPtr(true),
		ApplyImmediately:     boolPtr(false),
	}

	_, err := m.client.ModifyDBInstance(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to enable Multi-AZ: %w", err)
	}

	log.Printf("Successfully enabled Multi-AZ for: %s", dbInstanceID)
	return nil
}

func (m *MultiAZManager) DisableMultiAZ(dbInstanceID string) error {
	input := &rds.ModifyDBInstanceInput{
		DBInstanceIdentifier: &dbInstanceID,
		MultiAZ:              boolPtr(false),
		ApplyImmediately:     boolPtr(false),
	}

	_, err := m.client.ModifyDBInstance(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to disable Multi-AZ: %w", err)
	}

	log.Printf("Successfully disabled Multi-AZ for: %s", dbInstanceID)
	return nil
}

func boolPtr(b bool) *bool { return &b }

func main() {
	manager, err := NewMultiAZManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.EnableMultiAZ("autocloud-db")
	if err != nil {
		log.Fatal(err)
	}
}
