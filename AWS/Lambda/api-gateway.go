package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/apigateway"
	"github.com/aws/aws-sdk-go-v2/service/apigateway/types"
)

type APIGatewayManager struct {
	client *apigateway.Client
	ctx    context.Context
}

func NewAPIGatewayManager(region string) (*APIGatewayManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &APIGatewayManager{
		client: apigateway.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *APIGatewayManager) CreateRestAPI(name, description string) (string, error) {
	input := &apigateway.CreateRestApiInput{
		Name:        &name,
		Description: &description,
		EndpointConfiguration: &types.EndpointConfiguration{
			Types: []types.EndpointType{types.EndpointTypeRegional},
		},
	}

	result, err := m.client.CreateRestApi(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create REST API: %w", err)
	}

	apiID := *result.Id
	log.Printf("Successfully created REST API: %s", apiID)
	return apiID, nil
}

func (m *APIGatewayManager) CreateDeployment(apiID, stageName string) error {
	input := &apigateway.CreateDeploymentInput{
		RestApiId: &apiID,
		StageName: &stageName,
	}

	_, err := m.client.CreateDeployment(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to create deployment: %w", err)
	}

	log.Printf("Successfully deployed API to stage: %s", stageName)
	return nil
}

func (m *APIGatewayManager) DeleteRestAPI(apiID string) error {
	input := &apigateway.DeleteRestApiInput{
		RestApiId: &apiID,
	}

	_, err := m.client.DeleteRestApi(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete REST API: %w", err)
	}

	log.Printf("Successfully deleted REST API: %s", apiID)
	return nil
}

func main() {
	manager, err := NewAPIGatewayManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	apiID, err := manager.CreateRestAPI("autocloud-api", "AutoCloud REST API")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("API ID: %s\n", apiID)
}
