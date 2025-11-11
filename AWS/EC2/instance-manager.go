package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
)

type EC2Manager struct {
	client *ec2.Client
	ctx    context.Context
}

func NewEC2Manager(region string) (*EC2Manager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, fmt.Errorf("unable to load SDK config: %w", err)
	}

	return &EC2Manager{
		client: ec2.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *EC2Manager) LaunchInstance(amiID, instanceType, keyName string) (string, error) {
	input := &ec2.RunInstancesInput{
		ImageId:      &amiID,
		InstanceType: types.InstanceType(instanceType),
		KeyName:      &keyName,
		MinCount:     intPtr(1),
		MaxCount:     intPtr(1),
		TagSpecifications: []types.TagSpecification{
			{
				ResourceType: types.ResourceTypeInstance,
				Tags: []types.Tag{
					{
						Key:   strPtr("Name"),
						Value: strPtr("AutoCloud-Instance"),
					},
					{
						Key:   strPtr("ManagedBy"),
						Value: strPtr("AutoCloud"),
					},
				},
			},
		},
	}

	result, err := m.client.RunInstances(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to launch instance: %w", err)
	}

	instanceID := *result.Instances[0].InstanceId
	log.Printf("Successfully launched instance: %s", instanceID)
	return instanceID, nil
}

func (m *EC2Manager) TerminateInstance(instanceID string) error {
	input := &ec2.TerminateInstancesInput{
		InstanceIds: []string{instanceID},
	}

	_, err := m.client.TerminateInstances(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to terminate instance: %w", err)
	}

	log.Printf("Successfully terminated instance: %s", instanceID)
	return nil
}

func (m *EC2Manager) ListInstances() ([]types.Instance, error) {
	input := &ec2.DescribeInstancesInput{}
	result, err := m.client.DescribeInstances(m.ctx, input)
	if err != nil {
		return nil, fmt.Errorf("failed to list instances: %w", err)
	}

	var instances []types.Instance
	for _, reservation := range result.Reservations {
		instances = append(instances, reservation.Instances...)
	}

	return instances, nil
}

func strPtr(s string) *string {
	return &s
}

func intPtr(i int32) *int32 {
	return &i
}

func main() {
	manager, err := NewEC2Manager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	instances, err := manager.ListInstances()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Found %d instances\n", len(instances))
}
