package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/iam"
)

type IAMPolicyManager struct {
	client *iam.Client
	ctx    context.Context
}

func NewIAMPolicyManager(region string) (*IAMPolicyManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &IAMPolicyManager{
		client: iam.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *IAMPolicyManager) CreatePolicy(policyName, policyDocument string) (string, error) {
	input := &iam.CreatePolicyInput{
		PolicyName:     &policyName,
		PolicyDocument: &policyDocument,
	}

	result, err := m.client.CreatePolicy(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create policy: %w", err)
	}

	policyArn := *result.Policy.Arn
	log.Printf("Successfully created IAM policy: %s", policyName)
	return policyArn, nil
}

func (m *IAMPolicyManager) DeletePolicy(policyArn string) error {
	input := &iam.DeletePolicyInput{
		PolicyArn: &policyArn,
	}

	_, err := m.client.DeletePolicy(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete policy: %w", err)
	}

	log.Printf("Successfully deleted IAM policy: %s", policyArn)
	return nil
}

func (m *IAMPolicyManager) GetPolicy(policyArn string) error {
	input := &iam.GetPolicyInput{
		PolicyArn: &policyArn,
	}

	result, err := m.client.GetPolicy(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to get policy: %w", err)
	}

	log.Printf("Policy: %+v", result.Policy)
	return nil
}

func main() {
	manager, err := NewIAMPolicyManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	policyDoc := `{
		"Version": "2012-10-17",
		"Statement": [{
			"Effect": "Allow",
			"Action": "s3:GetObject",
			"Resource": "arn:aws:s3:::autocloud-bucket/*"
		}]
	}`

	policyArn, err := manager.CreatePolicy("autocloud-s3-read", policyDoc)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Policy ARN: %s\n", policyArn)
}
