package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
)

type SecurityGroupManager struct {
	client *ec2.Client
	ctx    context.Context
}

func NewSecurityGroupManager(region string) (*SecurityGroupManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &SecurityGroupManager{
		client: ec2.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *SecurityGroupManager) CreateSecurityGroup(name, description, vpcID string) (string, error) {
	input := &ec2.CreateSecurityGroupInput{
		GroupName:   &name,
		Description: &description,
		VpcId:       &vpcID,
	}

	result, err := m.client.CreateSecurityGroup(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create security group: %w", err)
	}

	groupID := *result.GroupId
	log.Printf("Successfully created security group: %s", groupID)
	return groupID, nil
}

func (m *SecurityGroupManager) AddIngressRule(groupID string, port int32, protocol, cidr string) error {
	input := &ec2.AuthorizeSecurityGroupIngressInput{
		GroupId: &groupID,
		IpPermissions: []types.IpPermission{
			{
				IpProtocol: &protocol,
				FromPort:   &port,
				ToPort:     &port,
				IpRanges: []types.IpRange{
					{
						CidrIp: &cidr,
					},
				},
			},
		},
	}

	_, err := m.client.AuthorizeSecurityGroupIngress(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to add ingress rule: %w", err)
	}

	log.Printf("Successfully added ingress rule to security group: %s", groupID)
	return nil
}

func main() {
	manager, err := NewSecurityGroupManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	groupID, err := manager.CreateSecurityGroup("autocloud-sg", "AutoCloud Security Group", "vpc-12345")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.AddIngressRule(groupID, 80, "tcp", "0.0.0.0/0")
	if err != nil {
		log.Fatal(err)
	}
}
