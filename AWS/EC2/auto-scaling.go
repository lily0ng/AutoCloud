package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/autoscaling"
	"github.com/aws/aws-sdk-go-v2/service/autoscaling/types"
)

type AutoScalingManager struct {
	client *autoscaling.Client
	ctx    context.Context
}

func NewAutoScalingManager(region string) (*AutoScalingManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &AutoScalingManager{
		client: autoscaling.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *AutoScalingManager) CreateAutoScalingGroup(name string, minSize, maxSize, desiredCapacity int32) error {
	input := &autoscaling.CreateAutoScalingGroupInput{
		AutoScalingGroupName: &name,
		MinSize:              &minSize,
		MaxSize:              &maxSize,
		DesiredCapacity:      &desiredCapacity,
		AvailabilityZones:    []string{"us-east-1a", "us-east-1b"},
		Tags: []types.Tag{
			{
				Key:   strPtr("Name"),
				Value: strPtr("AutoCloud-ASG"),
			},
		},
	}

	_, err := m.client.CreateAutoScalingGroup(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to create auto scaling group: %w", err)
	}

	log.Printf("Successfully created auto scaling group: %s", name)
	return nil
}

func (m *AutoScalingManager) UpdateAutoScalingGroup(name string, minSize, maxSize, desiredCapacity int32) error {
	input := &autoscaling.UpdateAutoScalingGroupInput{
		AutoScalingGroupName: &name,
		MinSize:              &minSize,
		MaxSize:              &maxSize,
		DesiredCapacity:      &desiredCapacity,
	}

	_, err := m.client.UpdateAutoScalingGroup(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to update auto scaling group: %w", err)
	}

	log.Printf("Successfully updated auto scaling group: %s", name)
	return nil
}

func (m *AutoScalingManager) DeleteAutoScalingGroup(name string, forceDelete bool) error {
	input := &autoscaling.DeleteAutoScalingGroupInput{
		AutoScalingGroupName: &name,
		ForceDelete:          &forceDelete,
	}

	_, err := m.client.DeleteAutoScalingGroup(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete auto scaling group: %w", err)
	}

	log.Printf("Successfully deleted auto scaling group: %s", name)
	return nil
}

func strPtr(s string) *string {
	return &s
}

func main() {
	manager, err := NewAutoScalingManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.CreateAutoScalingGroup("autocloud-asg", 2, 10, 3)
	if err != nil {
		log.Fatal(err)
	}
}
