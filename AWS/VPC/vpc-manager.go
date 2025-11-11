package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
)

type VPCManager struct {
	client *ec2.Client
	ctx    context.Context
}

func NewVPCManager(region string) (*VPCManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &VPCManager{
		client: ec2.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *VPCManager) CreateVPC(cidrBlock, name string) (string, error) {
	input := &ec2.CreateVpcInput{
		CidrBlock: &cidrBlock,
		TagSpecifications: []types.TagSpecification{
			{
				ResourceType: types.ResourceTypeVpc,
				Tags: []types.Tag{
					{
						Key:   strPtr("Name"),
						Value: &name,
					},
				},
			},
		},
	}

	result, err := m.client.CreateVpc(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create VPC: %w", err)
	}

	vpcID := *result.Vpc.VpcId
	log.Printf("Successfully created VPC: %s (%s)", vpcID, cidrBlock)

	// Enable DNS hostnames
	m.enableDNSHostnames(vpcID)

	return vpcID, nil
}

func (m *VPCManager) enableDNSHostnames(vpcID string) error {
	input := &ec2.ModifyVpcAttributeInput{
		VpcId:              &vpcID,
		EnableDnsHostnames: &types.AttributeBooleanValue{Value: boolPtr(true)},
	}

	_, err := m.client.ModifyVpcAttribute(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to enable DNS hostnames: %w", err)
	}

	log.Printf("Enabled DNS hostnames for VPC: %s", vpcID)
	return nil
}

func (m *VPCManager) DeleteVPC(vpcID string) error {
	input := &ec2.DeleteVpcInput{
		VpcId: &vpcID,
	}

	_, err := m.client.DeleteVpc(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete VPC: %w", err)
	}

	log.Printf("Successfully deleted VPC: %s", vpcID)
	return nil
}

func (m *VPCManager) ListVPCs() ([]types.Vpc, error) {
	input := &ec2.DescribeVpcsInput{}

	result, err := m.client.DescribeVpcs(m.ctx, input)
	if err != nil {
		return nil, fmt.Errorf("failed to list VPCs: %w", err)
	}

	return result.Vpcs, nil
}

func strPtr(s string) *string { return &s }
func boolPtr(b bool) *bool    { return &b }

func main() {
	manager, err := NewVPCManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	vpcID, err := manager.CreateVPC("10.0.0.0/16", "autocloud-vpc")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("VPC ID: %s\n", vpcID)
}
