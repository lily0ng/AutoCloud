package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/iam"
	"github.com/aws/aws-sdk-go-v2/service/iam/types"
)

type IAMRoleManager struct {
	client *iam.Client
	ctx    context.Context
}

func NewIAMRoleManager(region string) (*IAMRoleManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &IAMRoleManager{
		client: iam.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *IAMRoleManager) CreateRole(roleName, assumeRolePolicy string) (string, error) {
	input := &iam.CreateRoleInput{
		RoleName:                 &roleName,
		AssumeRolePolicyDocument: &assumeRolePolicy,
		Tags: []types.Tag{
			{
				Key:   strPtr("ManagedBy"),
				Value: strPtr("AutoCloud"),
			},
		},
	}

	result, err := m.client.CreateRole(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create role: %w", err)
	}

	roleArn := *result.Role.Arn
	log.Printf("Successfully created IAM role: %s", roleName)
	return roleArn, nil
}

func (m *IAMRoleManager) DeleteRole(roleName string) error {
	input := &iam.DeleteRoleInput{
		RoleName: &roleName,
	}

	_, err := m.client.DeleteRole(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete role: %w", err)
	}

	log.Printf("Successfully deleted IAM role: %s", roleName)
	return nil
}

func (m *IAMRoleManager) AttachPolicy(roleName, policyArn string) error {
	input := &iam.AttachRolePolicyInput{
		RoleName:  &roleName,
		PolicyArn: &policyArn,
	}

	_, err := m.client.AttachRolePolicy(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to attach policy: %w", err)
	}

	log.Printf("Successfully attached policy %s to role %s", policyArn, roleName)
	return nil
}

func strPtr(s string) *string { return &s }

func main() {
	manager, err := NewIAMRoleManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	assumeRolePolicy := `{
		"Version": "2012-10-17",
		"Statement": [{
			"Effect": "Allow",
			"Principal": {"Service": "ec2.amazonaws.com"},
			"Action": "sts:AssumeRole"
		}]
	}`

	roleArn, err := manager.CreateRole("autocloud-role", assumeRolePolicy)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Role ARN: %s\n", roleArn)
}
