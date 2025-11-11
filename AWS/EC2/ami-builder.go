package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
)

type AMIBuilder struct {
	client *ec2.Client
	ctx    context.Context
}

func NewAMIBuilder(region string) (*AMIBuilder, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &AMIBuilder{
		client: ec2.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (b *AMIBuilder) CreateAMI(instanceID, name, description string) (string, error) {
	input := &ec2.CreateImageInput{
		InstanceId:  &instanceID,
		Name:        &name,
		Description: &description,
	}

	result, err := b.client.CreateImage(b.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create AMI: %w", err)
	}

	amiID := *result.ImageId
	log.Printf("Successfully created AMI: %s", amiID)
	return amiID, nil
}

func (b *AMIBuilder) DeregisterAMI(amiID string) error {
	input := &ec2.DeregisterImageInput{
		ImageId: &amiID,
	}

	_, err := b.client.DeregisterImage(b.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to deregister AMI: %w", err)
	}

	log.Printf("Successfully deregister AMI: %s", amiID)
	return nil
}

func main() {
	builder, err := NewAMIBuilder("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	amiID, err := builder.CreateAMI("i-1234567890abcdef0", "autocloud-ami", "AutoCloud AMI")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Created AMI: %s\n", amiID)
}
