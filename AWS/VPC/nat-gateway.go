package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
)

type NATGatewayManager struct {
	client *ec2.Client
	ctx    context.Context
}

func NewNATGatewayManager(region string) (*NATGatewayManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &NATGatewayManager{
		client: ec2.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *NATGatewayManager) CreateNATGateway(subnetID, allocationID, name string) (string, error) {
	input := &ec2.CreateNatGatewayInput{
		SubnetId:     &subnetID,
		AllocationId: &allocationID,
		TagSpecifications: []types.TagSpecification{
			{
				ResourceType: types.ResourceTypeNatgateway,
				Tags: []types.Tag{
					{
						Key:   strPtr("Name"),
						Value: &name,
					},
				},
			},
		},
	}

	result, err := m.client.CreateNatGateway(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create NAT gateway: %w", err)
	}

	natGatewayID := *result.NatGateway.NatGatewayId
	log.Printf("Successfully created NAT gateway: %s", natGatewayID)

	// Wait for NAT gateway to become available
	log.Printf("Waiting for NAT gateway to become available...")
	m.waitForNATGateway(natGatewayID)

	return natGatewayID, nil
}

func (m *NATGatewayManager) waitForNATGateway(natGatewayID string) error {
	waiter := ec2.NewNatGatewayAvailableWaiter(m.client)
	input := &ec2.DescribeNatGatewaysInput{
		NatGatewayIds: []string{natGatewayID},
	}

	maxWaitTime := 5 * time.Minute
	err := waiter.Wait(m.ctx, input, maxWaitTime)
	if err != nil {
		return fmt.Errorf("failed waiting for NAT gateway: %w", err)
	}

	log.Printf("NAT gateway %s is now available", natGatewayID)
	return nil
}

func (m *NATGatewayManager) DeleteNATGateway(natGatewayID string) error {
	input := &ec2.DeleteNatGatewayInput{
		NatGatewayId: &natGatewayID,
	}

	_, err := m.client.DeleteNatGateway(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete NAT gateway: %w", err)
	}

	log.Printf("Successfully deleted NAT gateway: %s", natGatewayID)
	return nil
}

func strPtr(s string) *string { return &s }

func main() {
	manager, err := NewNATGatewayManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	natID, err := manager.CreateNATGateway(
		"subnet-12345",
		"eipalloc-12345",
		"autocloud-nat",
	)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("NAT Gateway ID: %s\n", natID)
}
