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

type LambdaManager struct {
	client *lambda.Client
	ctx    context.Context
}

func NewLambdaManager(region string) (*LambdaManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &LambdaManager{
		client: lambda.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *LambdaManager) CreateFunction(functionName, roleArn, handler, runtime, zipFile string) error {
	code, err := os.ReadFile(zipFile)
	if err != nil {
		return fmt.Errorf("failed to read zip file: %w", err)
	}

	input := &lambda.CreateFunctionInput{
		FunctionName: &functionName,
		Runtime:      types.Runtime(runtime),
		Role:         &roleArn,
		Handler:      &handler,
		Code: &types.FunctionCode{
			ZipFile: code,
		},
		Timeout:     intPtr(30),
		MemorySize:  intPtr(256),
		Description: strPtr("AutoCloud Lambda function"),
	}

	_, err = m.client.CreateFunction(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to create function: %w", err)
	}

	log.Printf("Successfully created Lambda function: %s", functionName)
	return nil
}

func (m *LambdaManager) UpdateFunctionCode(functionName, zipFile string) error {
	code, err := os.ReadFile(zipFile)
	if err != nil {
		return fmt.Errorf("failed to read zip file: %w", err)
	}

	input := &lambda.UpdateFunctionCodeInput{
		FunctionName: &functionName,
		ZipFile:      code,
	}

	_, err = m.client.UpdateFunctionCode(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to update function code: %w", err)
	}

	log.Printf("Successfully updated Lambda function: %s", functionName)
	return nil
}

func (m *LambdaManager) DeleteFunction(functionName string) error {
	input := &lambda.DeleteFunctionInput{
		FunctionName: &functionName,
	}

	_, err := m.client.DeleteFunction(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete function: %w", err)
	}

	log.Printf("Successfully deleted Lambda function: %s", functionName)
	return nil
}

func (m *LambdaManager) InvokeFunction(functionName string, payload []byte) ([]byte, error) {
	input := &lambda.InvokeInput{
		FunctionName: &functionName,
		Payload:      payload,
	}

	result, err := m.client.Invoke(m.ctx, input)
	if err != nil {
		return nil, fmt.Errorf("failed to invoke function: %w", err)
	}

	return result.Payload, nil
}

func strPtr(s string) *string { return &s }
func intPtr(i int32) *int32   { return &i }

func main() {
	manager, err := NewLambdaManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.CreateFunction(
		"autocloud-function",
		"arn:aws:iam::123456789:role/lambda-role",
		"index.handler",
		"nodejs18.x",
		"function.zip",
	)
	if err != nil {
		log.Fatal(err)
	}
}
