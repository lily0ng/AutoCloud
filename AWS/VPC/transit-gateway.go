package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
)

type TransitGatewayManager struct {
	client *ec2.Client
	ctx    context.Context
}

func NewTransitGatewayManager(region string) (*TransitGatewayManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &TransitGatewayManager{
		client: ec2.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *TransitGatewayManager) CreateTransitGateway(description string) (string, error) {
	input := &ec2.CreateTransitGatewayInput{
		Description: &description,
		Options: &types.TransitGatewayRequestOptions{
			DefaultRouteTableAssociation: types.DefaultRouteTableAssociationValueEnable,
			DefaultRouteTablePropagation: types.DefaultRouteTablePropagationValueEnable,
			DnsSupport:                   types.DnsSupportValueEnable,
			VpnEcmpSupport:              types.VpnEcmpSupportValueEnable,
		},
		TagSpecifications: []types.TagSpecification{
			{
				ResourceType: types.ResourceTypeTransitGateway,
				Tags: []types.Tag{
					{
						Key:   strPtr("Name"),
						Value: strPtr("autocloud-tgw"),
					},
				},
			},
		},
	}

	result, err := m.client.CreateTransitGateway(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create transit gateway: %w", err)
	}

	tgwID := *result.TransitGateway.TransitGatewayId
	log.Printf("Successfully created transit gateway: %s", tgwID)
	return tgwID, nil
}

func (m *TransitGatewayManager) AttachVPC(tgwID, vpcID string, subnetIDs []string) (string, error) {
	input := &ec2.CreateTransitGatewayVpcAttachmentInput{
		TransitGatewayId: &tgwID,
		VpcId:            &vpcID,
		SubnetIds:        subnetIDs,
		TagSpecifications: []types.TagSpecification{
			{
				ResourceType: types.ResourceTypeTransitGatewayAttachment,
				Tags: []types.Tag{
					{
						Key:   strPtr("Name"),
						Value: strPtr("autocloud-tgw-attachment"),
					},
				},
			},
		},
	}

	result, err := m.client.CreateTransitGatewayVpcAttachment(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to attach VPC to transit gateway: %w", err)
	}

	attachmentID := *result.TransitGatewayVpcAttachment.TransitGatewayAttachmentId
	log.Printf("Successfully attached VPC %s to transit gateway %s", vpcID, tgwID)
	return attachmentID, nil
}

func (m *TransitGatewayManager) DeleteTransitGateway(tgwID string) error {
	input := &ec2.DeleteTransitGatewayInput{
		TransitGatewayId: &tgwID,
	}

	_, err := m.client.DeleteTransitGateway(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete transit gateway: %w", err)
	}

	log.Printf("Successfully deleted transit gateway: %s", tgwID)
	return nil
}

func strPtr(s string) *string { return &s }

func main() {
	manager, err := NewTransitGatewayManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	tgwID, err := manager.CreateTransitGateway("AutoCloud Transit Gateway")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Transit Gateway ID: %s\n", tgwID)
}
