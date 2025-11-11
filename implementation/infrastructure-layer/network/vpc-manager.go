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

func (v *VPCManager) CreateVPC(cidrBlock string, name string) (string, error) {
	input := &ec2.CreateVpcInput{
		CidrBlock: &cidrBlock,
		TagSpecifications: []types.TagSpecification{
			{
				ResourceType: types.ResourceTypeVpc,
				Tags: []types.Tag{
					{
						Key:   stringPtr("Name"),
						Value: &name,
					},
				},
			},
		},
	}

	result, err := v.client.CreateVpc(v.ctx, input)
	if err != nil {
		return "", err
	}

	vpcID := *result.Vpc.VpcId
	log.Printf("VPC created: %s", vpcID)
	return vpcID, nil
}

func (v *VPCManager) CreateSubnet(vpcID, cidrBlock, az, name string) (string, error) {
	input := &ec2.CreateSubnetInput{
		VpcId:            &vpcID,
		CidrBlock:        &cidrBlock,
		AvailabilityZone: &az,
		TagSpecifications: []types.TagSpecification{
			{
				ResourceType: types.ResourceTypeSubnet,
				Tags: []types.Tag{
					{
						Key:   stringPtr("Name"),
						Value: &name,
					},
				},
			},
		},
	}

	result, err := v.client.CreateSubnet(v.ctx, input)
	if err != nil {
		return "", err
	}

	subnetID := *result.Subnet.SubnetId
	log.Printf("Subnet created: %s", subnetID)
	return subnetID, nil
}

func (v *VPCManager) CreateInternetGateway(name string) (string, error) {
	input := &ec2.CreateInternetGatewayInput{
		TagSpecifications: []types.TagSpecification{
			{
				ResourceType: types.ResourceTypeInternetGateway,
				Tags: []types.Tag{
					{
						Key:   stringPtr("Name"),
						Value: &name,
					},
				},
			},
		},
	}

	result, err := v.client.CreateInternetGateway(v.ctx, input)
	if err != nil {
		return "", err
	}

	igwID := *result.InternetGateway.InternetGatewayId
	log.Printf("Internet Gateway created: %s", igwID)
	return igwID, nil
}

func (v *VPCManager) AttachInternetGateway(vpcID, igwID string) error {
	input := &ec2.AttachInternetGatewayInput{
		VpcId:             &vpcID,
		InternetGatewayId: &igwID,
	}

	_, err := v.client.AttachInternetGateway(v.ctx, input)
	if err != nil {
		return err
	}

	log.Printf("Internet Gateway %s attached to VPC %s", igwID, vpcID)
	return nil
}

func stringPtr(s string) *string {
	return &s
}

func main() {
	manager, err := NewVPCManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	vpcID, err := manager.CreateVPC("10.0.0.0/16", "AutoCloud-VPC")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("VPC Created: %s\n", vpcID)
}
