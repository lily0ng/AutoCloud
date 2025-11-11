package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
)

type VPCPeeringManager struct {
	client *ec2.Client
	ctx    context.Context
}

func NewVPCPeeringManager(region string) (*VPCPeeringManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &VPCPeeringManager{
		client: ec2.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *VPCPeeringManager) CreatePeeringConnection(vpcID, peerVpcID, name string) (string, error) {
	input := &ec2.CreateVpcPeeringConnectionInput{
		VpcId:     &vpcID,
		PeerVpcId: &peerVpcID,
		TagSpecifications: []types.TagSpecification{
			{
				ResourceType: types.ResourceTypeVpcPeeringConnection,
				Tags: []types.Tag{
					{
						Key:   strPtr("Name"),
						Value: &name,
					},
				},
			},
		},
	}

	result, err := m.client.CreateVpcPeeringConnection(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create VPC peering connection: %w", err)
	}

	peeringID := *result.VpcPeeringConnection.VpcPeeringConnectionId
	log.Printf("Successfully created VPC peering connection: %s", peeringID)
	return peeringID, nil
}

func (m *VPCPeeringManager) AcceptPeeringConnection(peeringID string) error {
	input := &ec2.AcceptVpcPeeringConnectionInput{
		VpcPeeringConnectionId: &peeringID,
	}

	_, err := m.client.AcceptVpcPeeringConnection(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to accept VPC peering connection: %w", err)
	}

	log.Printf("Successfully accepted VPC peering connection: %s", peeringID)
	return nil
}

func (m *VPCPeeringManager) DeletePeeringConnection(peeringID string) error {
	input := &ec2.DeleteVpcPeeringConnectionInput{
		VpcPeeringConnectionId: &peeringID,
	}

	_, err := m.client.DeleteVpcPeeringConnection(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete VPC peering connection: %w", err)
	}

	log.Printf("Successfully deleted VPC peering connection: %s", peeringID)
	return nil
}

func strPtr(s string) *string { return &s }

func main() {
	manager, err := NewVPCPeeringManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	peeringID, err := manager.CreatePeeringConnection(
		"vpc-12345",
		"vpc-67890",
		"autocloud-peering",
	)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("VPC Peering Connection ID: %s\n", peeringID)
}
