package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
)

type PlacementGroupManager struct {
	client *ec2.Client
	ctx    context.Context
}

func NewPlacementGroupManager(region string) (*PlacementGroupManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &PlacementGroupManager{
		client: ec2.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *PlacementGroupManager) CreatePlacementGroup(name string, strategy types.PlacementStrategy) error {
	input := &ec2.CreatePlacementGroupInput{
		GroupName: &name,
		Strategy:  strategy,
	}

	_, err := m.client.CreatePlacementGroup(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to create placement group: %w", err)
	}

	log.Printf("Successfully created placement group: %s", name)
	return nil
}

func (m *PlacementGroupManager) DeletePlacementGroup(name string) error {
	input := &ec2.DeletePlacementGroupInput{
		GroupName: &name,
	}

	_, err := m.client.DeletePlacementGroup(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete placement group: %w", err)
	}

	log.Printf("Successfully deleted placement group: %s", name)
	return nil
}

func main() {
	manager, err := NewPlacementGroupManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.CreatePlacementGroup("autocloud-pg", types.PlacementStrategyCluster)
	if err != nil {
		log.Fatal(err)
	}
}
