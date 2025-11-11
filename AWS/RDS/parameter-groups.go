package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/rds"
	"github.com/aws/aws-sdk-go-v2/service/rds/types"
)

type ParameterGroupManager struct {
	client *rds.Client
	ctx    context.Context
}

func NewParameterGroupManager(region string) (*ParameterGroupManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &ParameterGroupManager{
		client: rds.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *ParameterGroupManager) CreateParameterGroup(name, family, description string) error {
	input := &rds.CreateDBParameterGroupInput{
		DBParameterGroupName:   &name,
		DBParameterGroupFamily: &family,
		Description:            &description,
	}

	_, err := m.client.CreateDBParameterGroup(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to create parameter group: %w", err)
	}

	log.Printf("Successfully created parameter group: %s", name)
	return nil
}

func (m *ParameterGroupManager) ModifyParameters(groupName string, parameters []types.Parameter) error {
	input := &rds.ModifyDBParameterGroupInput{
		DBParameterGroupName: &groupName,
		Parameters:           parameters,
	}

	_, err := m.client.ModifyDBParameterGroup(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to modify parameters: %w", err)
	}

	log.Printf("Successfully modified parameter group: %s", groupName)
	return nil
}

func main() {
	manager, err := NewParameterGroupManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.CreateParameterGroup("autocloud-params", "postgres14", "AutoCloud parameter group")
	if err != nil {
		log.Fatal(err)
	}
}
