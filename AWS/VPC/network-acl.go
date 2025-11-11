package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
)

type NetworkACLManager struct {
	client *ec2.Client
	ctx    context.Context
}

func NewNetworkACLManager(region string) (*NetworkACLManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &NetworkACLManager{
		client: ec2.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *NetworkACLManager) CreateNetworkACL(vpcID, name string) (string, error) {
	input := &ec2.CreateNetworkAclInput{
		VpcId: &vpcID,
		TagSpecifications: []types.TagSpecification{
			{
				ResourceType: types.ResourceTypeNetworkAcl,
				Tags: []types.Tag{{Key: strPtr("Name"), Value: &name}},
			},
		},
	}

	result, err := m.client.CreateNetworkAcl(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create network ACL: %w", err)
	}

	aclID := *result.NetworkAcl.NetworkAclId
	log.Printf("Created network ACL: %s", aclID)
	return aclID, nil
}

func strPtr(s string) *string { return &s }

func main() {
	manager, err := NewNetworkACLManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	aclID, err := manager.CreateNetworkACL("vpc-12345", "autocloud-acl")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Network ACL ID: %s\n", aclID)
}
