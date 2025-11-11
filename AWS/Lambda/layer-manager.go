package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/lambda"
	"github.com/aws/aws-sdk-go-v2/service/lambda/types"
)

type LayerManager struct {
	client *lambda.Client
	ctx    context.Context
}

func NewLayerManager(region string) (*LayerManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &LayerManager{
		client: lambda.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *LayerManager) PublishLayer(layerName, description, zipFile string, compatibleRuntimes []types.Runtime) (string, error) {
	code, err := os.ReadFile(zipFile)
	if err != nil {
		return "", fmt.Errorf("failed to read zip file: %w", err)
	}

	input := &lambda.PublishLayerVersionInput{
		LayerName:          &layerName,
		Description:        &description,
		Content:            &types.LayerVersionContentInput{ZipFile: code},
		CompatibleRuntimes: compatibleRuntimes,
	}

	result, err := m.client.PublishLayerVersion(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to publish layer: %w", err)
	}

	layerArn := *result.LayerVersionArn
	log.Printf("Successfully published layer: %s", layerArn)
	return layerArn, nil
}

func (m *LayerManager) DeleteLayerVersion(layerName string, versionNumber int64) error {
	input := &lambda.DeleteLayerVersionInput{
		LayerName:     &layerName,
		VersionNumber: &versionNumber,
	}

	_, err := m.client.DeleteLayerVersion(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete layer version: %w", err)
	}

	log.Printf("Successfully deleted layer version: %s:%d", layerName, versionNumber)
	return nil
}

func main() {
	manager, err := NewLayerManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	layerArn, err := manager.PublishLayer(
		"autocloud-layer",
		"AutoCloud dependencies layer",
		"layer.zip",
		[]types.Runtime{types.RuntimeNodejs18x, types.RuntimePython39},
	)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Layer ARN: %s\n", layerArn)
}
