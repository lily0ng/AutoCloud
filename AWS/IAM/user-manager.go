package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/iam"
	"github.com/aws/aws-sdk-go-v2/service/iam/types"
)

type IAMUserManager struct {
	client *iam.Client
	ctx    context.Context
}

func NewIAMUserManager(region string) (*IAMUserManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &IAMUserManager{
		client: iam.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *IAMUserManager) CreateUser(username string) error {
	input := &iam.CreateUserInput{
		UserName: &username,
		Tags: []types.Tag{
			{
				Key:   strPtr("ManagedBy"),
				Value: strPtr("AutoCloud"),
			},
		},
	}

	_, err := m.client.CreateUser(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to create user: %w", err)
	}

	log.Printf("Successfully created IAM user: %s", username)
	return nil
}

func (m *IAMUserManager) DeleteUser(username string) error {
	input := &iam.DeleteUserInput{
		UserName: &username,
	}

	_, err := m.client.DeleteUser(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete user: %w", err)
	}

	log.Printf("Successfully deleted IAM user: %s", username)
	return nil
}

func (m *IAMUserManager) ListUsers() ([]types.User, error) {
	input := &iam.ListUsersInput{}

	result, err := m.client.ListUsers(m.ctx, input)
	if err != nil {
		return nil, fmt.Errorf("failed to list users: %w", err)
	}

	return result.Users, nil
}

func (m *IAMUserManager) AttachPolicy(username, policyArn string) error {
	input := &iam.AttachUserPolicyInput{
		UserName:  &username,
		PolicyArn: &policyArn,
	}

	_, err := m.client.AttachUserPolicy(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to attach policy: %w", err)
	}

	log.Printf("Successfully attached policy %s to user %s", policyArn, username)
	return nil
}

func strPtr(s string) *string { return &s }

func main() {
	manager, err := NewIAMUserManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = manager.CreateUser("autocloud-user")
	if err != nil {
		log.Fatal(err)
	}
}
