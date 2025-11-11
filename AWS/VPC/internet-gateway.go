package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
)

type InternetGatewayManager struct {
	client *ec2.Client
	ctx    context.Context
}

func NewInternetGatewayManager(region string) (*InternetGatewayManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &InternetGatewayManager{
		client: ec2.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *InternetGatewayManager) CreateInternetGateway(name string) (string, error) {
	input := &ec2.CreateInternetGatewayInput{
		TagSpecifications: []types.TagSpecification{
			{
				ResourceType: types.ResourceTypeInternetGateway,
				Tags: []types.Tag{
					{
						Key:   strPtr("Name"),
						Value: &name,
					},
				},
			},
		},
	}

	result, err := m.client.CreateInternetGateway(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create internet gateway: %w", err)
	}

	igwID := *result.InternetGateway.InternetGatewayId
	log.Printf("Successfully created internet gateway: %s", igwID)
	return igwID, nil
}

func (m *InternetGatewayManager) AttachToVPC(igwID, vpcID string) error {
	input := &ec2.AttachInternetGatewayInput{
		InternetGatewayId: &igwID,
		VpcId:             &vpcID,
	}

	_, err := m.client.AttachInternetGateway(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to attach internet gateway: %w", err)
	}

	log.Printf("Successfully attached internet gateway %s to VPC %s", igwID, vpcID)
	return nil
}

func (m *InternetGatewayManager) DetachFromVPC(igwID, vpcID string) error {
	input := &ec2.DetachInternetGatewayInput{
		InternetGatewayId: &igwID,
		VpcId:             &vpcID,
	}

	_, err := m.client.DetachInternetGateway(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to detach internet gateway: %w", err)
	}

	log.Printf("Successfully detached internet gateway %s from VPC %s", igwID, vpcID)
	return nil
}

func (m *InternetGatewayManager) DeleteInternetGateway(igwID string) error {
	input := &ec2.DeleteInternetGatewayInput{
		InternetGatewayId: &igwID,
	}

	_, err := m.client.DeleteInternetGateway(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete internet gateway: %w", err)
	}

	log.Printf("Successfully deleted internet gateway: %s", igwID)
	return nil
}

func strPtr(s string) *string { return &s }

func main() {
	manager, err := NewInternetGatewayManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	igwID, err := manager.CreateInternetGateway("autocloud-igw")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.AttachToVPC(igwID, "vpc-12345")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Internet Gateway ID: %s\n", igwID)
}
