package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
)

type ElasticIPManager struct {
	client *ec2.Client
	ctx    context.Context
}

func NewElasticIPManager(region string) (*ElasticIPManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &ElasticIPManager{
		client: ec2.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *ElasticIPManager) AllocateElasticIP() (string, string, error) {
	input := &ec2.AllocateAddressInput{
		Domain: types.DomainTypeVpc,
	}

	result, err := m.client.AllocateAddress(m.ctx, input)
	if err != nil {
		return "", "", fmt.Errorf("failed to allocate elastic IP: %w", err)
	}

	allocationID := *result.AllocationId
	publicIP := *result.PublicIp
	log.Printf("Successfully allocated elastic IP: %s (%s)", publicIP, allocationID)
	return allocationID, publicIP, nil
}

func (m *ElasticIPManager) AssociateElasticIP(allocationID, instanceID string) error {
	input := &ec2.AssociateAddressInput{
		AllocationId: &allocationID,
		InstanceId:   &instanceID,
	}

	_, err := m.client.AssociateAddress(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to associate elastic IP: %w", err)
	}

	log.Printf("Successfully associated elastic IP to instance: %s", instanceID)
	return nil
}

func (m *ElasticIPManager) ReleaseElasticIP(allocationID string) error {
	input := &ec2.ReleaseAddressInput{
		AllocationId: &allocationID,
	}

	_, err := m.client.ReleaseAddress(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to release elastic IP: %w", err)
	}

	log.Printf("Successfully released elastic IP: %s", allocationID)
	return nil
}

func main() {
	manager, err := NewElasticIPManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	allocationID, publicIP, err := manager.AllocateElasticIP()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Allocated Elastic IP: %s (%s)\n", publicIP, allocationID)
}
