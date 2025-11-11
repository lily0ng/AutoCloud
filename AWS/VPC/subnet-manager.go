package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
)

type SubnetManager struct {
	client *ec2.Client
	ctx    context.Context
}

func NewSubnetManager(region string) (*SubnetManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &SubnetManager{
		client: ec2.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *SubnetManager) CreateSubnet(vpcID, cidrBlock, availabilityZone, name string, public bool) (string, error) {
	input := &ec2.CreateSubnetInput{
		VpcId:            &vpcID,
		CidrBlock:        &cidrBlock,
		AvailabilityZone: &availabilityZone,
		TagSpecifications: []types.TagSpecification{
			{
				ResourceType: types.ResourceTypeSubnet,
				Tags: []types.Tag{
					{
						Key:   strPtr("Name"),
						Value: &name,
					},
					{
						Key:   strPtr("Type"),
						Value: strPtr(map[bool]string{true: "Public", false: "Private"}[public]),
					},
				},
			},
		},
	}

	result, err := m.client.CreateSubnet(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create subnet: %w", err)
	}

	subnetID := *result.Subnet.SubnetId
	log.Printf("Successfully created subnet: %s (%s)", subnetID, cidrBlock)

	// Enable auto-assign public IP for public subnets
	if public {
		m.enableAutoAssignPublicIP(subnetID)
	}

	return subnetID, nil
}

func (m *SubnetManager) enableAutoAssignPublicIP(subnetID string) error {
	input := &ec2.ModifySubnetAttributeInput{
		SubnetId:            &subnetID,
		MapPublicIpOnLaunch: &types.AttributeBooleanValue{Value: boolPtr(true)},
	}

	_, err := m.client.ModifySubnetAttribute(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to enable auto-assign public IP: %w", err)
	}

	log.Printf("Enabled auto-assign public IP for subnet: %s", subnetID)
	return nil
}

func (m *SubnetManager) DeleteSubnet(subnetID string) error {
	input := &ec2.DeleteSubnetInput{
		SubnetId: &subnetID,
	}

	_, err := m.client.DeleteSubnet(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete subnet: %w", err)
	}

	log.Printf("Successfully deleted subnet: %s", subnetID)
	return nil
}

func (m *SubnetManager) ListSubnets(vpcID string) ([]types.Subnet, error) {
	input := &ec2.DescribeSubnetsInput{
		Filters: []types.Filter{
			{
				Name:   strPtr("vpc-id"),
				Values: []string{vpcID},
			},
		},
	}

	result, err := m.client.DescribeSubnets(m.ctx, input)
	if err != nil {
		return nil, fmt.Errorf("failed to list subnets: %w", err)
	}

	return result.Subnets, nil
}

func strPtr(s string) *string { return &s }
func boolPtr(b bool) *bool    { return &b }

func main() {
	manager, err := NewSubnetManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	subnetID, err := manager.CreateSubnet(
		"vpc-12345",
		"10.0.1.0/24",
		"us-east-1a",
		"autocloud-public-subnet",
		true,
	)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Subnet ID: %s\n", subnetID)
}
