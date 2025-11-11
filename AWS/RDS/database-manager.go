package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/rds"
	"github.com/aws/aws-sdk-go-v2/service/rds/types"
)

type RDSManager struct {
	client *rds.Client
	ctx    context.Context
}

func NewRDSManager(region string) (*RDSManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &RDSManager{
		client: rds.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *RDSManager) CreateDatabase(dbName, instanceClass, engine, username, password string) error {
	input := &rds.CreateDBInstanceInput{
		DBInstanceIdentifier: &dbName,
		DBInstanceClass:      &instanceClass,
		Engine:               &engine,
		MasterUsername:       &username,
		MasterUserPassword:   &password,
		AllocatedStorage:     intPtr(20),
		StorageType:          strPtr("gp2"),
		BackupRetentionPeriod: intPtr(7),
		MultiAZ:              boolPtr(true),
		PubliclyAccessible:   boolPtr(false),
	}

	_, err := m.client.CreateDBInstance(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to create database: %w", err)
	}

	log.Printf("Successfully created database: %s", dbName)
	return nil
}

func (m *RDSManager) DeleteDatabase(dbName string, skipFinalSnapshot bool) error {
	input := &rds.DeleteDBInstanceInput{
		DBInstanceIdentifier: &dbName,
		SkipFinalSnapshot:    &skipFinalSnapshot,
	}

	_, err := m.client.DeleteDBInstance(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete database: %w", err)
	}

	log.Printf("Successfully deleted database: %s", dbName)
	return nil
}

func (m *RDSManager) ListDatabases() ([]types.DBInstance, error) {
	input := &rds.DescribeDBInstancesInput{}
	result, err := m.client.DescribeDBInstances(m.ctx, input)
	if err != nil {
		return nil, fmt.Errorf("failed to list databases: %w", err)
	}

	return result.DBInstances, nil
}

func strPtr(s string) *string   { return &s }
func intPtr(i int32) *int32     { return &i }
func boolPtr(b bool) *bool      { return &b }

func main() {
	manager, err := NewRDSManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.CreateDatabase("autocloud-db", "db.t3.micro", "postgres", "admin", "password123")
	if err != nil {
		log.Fatal(err)
	}
}
