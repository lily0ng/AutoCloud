package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/lambda"
)

type EventSourceManager struct {
	client *lambda.Client
	ctx    context.Context
}

func NewEventSourceManager(region string) (*EventSourceManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &EventSourceManager{
		client: lambda.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *EventSourceManager) CreateEventSourceMapping(functionName, eventSourceArn string, batchSize int32) (string, error) {
	input := &lambda.CreateEventSourceMappingInput{
		FunctionName:   &functionName,
		EventSourceArn: &eventSourceArn,
		BatchSize:      &batchSize,
		Enabled:        boolPtr(true),
	}

	result, err := m.client.CreateEventSourceMapping(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create event source mapping: %w", err)
	}

	uuid := *result.UUID
	log.Printf("Successfully created event source mapping: %s", uuid)
	return uuid, nil
}

func (m *EventSourceManager) DeleteEventSourceMapping(uuid string) error {
	input := &lambda.DeleteEventSourceMappingInput{
		UUID: &uuid,
	}

	_, err := m.client.DeleteEventSourceMapping(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete event source mapping: %w", err)
	}

	log.Printf("Successfully deleted event source mapping: %s", uuid)
	return nil
}

func boolPtr(b bool) *bool { return &b }

func main() {
	manager, err := NewEventSourceManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	uuid, err := manager.CreateEventSourceMapping(
		"autocloud-function",
		"arn:aws:sqs:us-east-1:123456789:my-queue",
		10,
	)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Event Source Mapping UUID: %s\n", uuid)
}
