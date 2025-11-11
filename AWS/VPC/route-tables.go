package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
)

type RouteTableManager struct {
	client *ec2.Client
	ctx    context.Context
}

func NewRouteTableManager(region string) (*RouteTableManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &RouteTableManager{
		client: ec2.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *RouteTableManager) CreateRouteTable(vpcID, name string) (string, error) {
	input := &ec2.CreateRouteTableInput{
		VpcId: &vpcID,
		TagSpecifications: []types.TagSpecification{
			{
				ResourceType: types.ResourceTypeRouteTable,
				Tags: []types.Tag{
					{
						Key:   strPtr("Name"),
						Value: &name,
					},
				},
			},
		},
	}

	result, err := m.client.CreateRouteTable(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create route table: %w", err)
	}

	routeTableID := *result.RouteTable.RouteTableId
	log.Printf("Successfully created route table: %s", routeTableID)
	return routeTableID, nil
}

func (m *RouteTableManager) CreateRoute(routeTableID, destinationCIDR, gatewayID string) error {
	input := &ec2.CreateRouteInput{
		RouteTableId:         &routeTableID,
		DestinationCidrBlock: &destinationCIDR,
		GatewayId:            &gatewayID,
	}

	_, err := m.client.CreateRoute(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to create route: %w", err)
	}

	log.Printf("Successfully created route: %s -> %s", destinationCIDR, gatewayID)
	return nil
}

func (m *RouteTableManager) AssociateSubnet(routeTableID, subnetID string) (string, error) {
	input := &ec2.AssociateRouteTableInput{
		RouteTableId: &routeTableID,
		SubnetId:     &subnetID,
	}

	result, err := m.client.AssociateRouteTable(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to associate route table: %w", err)
	}

	associationID := *result.AssociationId
	log.Printf("Successfully associated route table %s with subnet %s", routeTableID, subnetID)
	return associationID, nil
}

func (m *RouteTableManager) DeleteRouteTable(routeTableID string) error {
	input := &ec2.DeleteRouteTableInput{
		RouteTableId: &routeTableID,
	}

	_, err := m.client.DeleteRouteTable(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete route table: %w", err)
	}

	log.Printf("Successfully deleted route table: %s", routeTableID)
	return nil
}

func strPtr(s string) *string { return &s }

func main() {
	manager, err := NewRouteTableManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	rtID, err := manager.CreateRouteTable("vpc-12345", "autocloud-public-rt")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Route Table ID: %s\n", rtID)
}
