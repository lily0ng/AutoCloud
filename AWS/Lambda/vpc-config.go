package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/lambda"
	"github.com/aws/aws-sdk-go-v2/service/lambda/types"
)

type LambdaVPCConfig struct {
	client *lambda.Client
	ctx    context.Context
}

func NewLambdaVPCConfig(region string) (*LambdaVPCConfig, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &LambdaVPCConfig{
		client: lambda.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *LambdaVPCConfig) UpdateVPCConfig(functionName string, subnetIds, securityGroupIds []string) error {
	input := &lambda.UpdateFunctionConfigurationInput{
		FunctionName: &functionName,
		VpcConfig: &types.VpcConfig{
			SubnetIds:        subnetIds,
			SecurityGroupIds: securityGroupIds,
		},
	}

	_, err := m.client.UpdateFunctionConfiguration(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to update VPC config: %w", err)
	}

	log.Printf("Successfully updated VPC config for function: %s", functionName)
	return nil
}

func (m *LambdaVPCConfig) RemoveVPCConfig(functionName string) error {
	input := &lambda.UpdateFunctionConfigurationInput{
		FunctionName: &functionName,
		VpcConfig: &types.VpcConfig{
			SubnetIds:        []string{},
			SecurityGroupIds: []string{},
		},
	}

	_, err := m.client.UpdateFunctionConfiguration(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to remove VPC config: %w", err)
	}

	log.Printf("Successfully removed VPC config from function: %s", functionName)
	return nil
}

func main() {
	manager, err := NewLambdaVPCConfig("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.UpdateVPCConfig(
		"autocloud-function",
		[]string{"subnet-12345", "subnet-67890"},
		[]string{"sg-12345"},
	)
	if err != nil {
		log.Fatal(err)
	}
}
