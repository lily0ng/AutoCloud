package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/iam"
)

type MFAEnforcer struct {
	client *iam.Client
	ctx    context.Context
}

func NewMFAEnforcer(region string) (*MFAEnforcer, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &MFAEnforcer{
		client: iam.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *MFAEnforcer) EnableVirtualMFA(username, serialNumber string) error {
	input := &iam.EnableMFADeviceInput{
		UserName:         &username,
		SerialNumber:     &serialNumber,
		AuthenticationCode1: strPtr("123456"),
		AuthenticationCode2: strPtr("654321"),
	}

	_, err := m.client.EnableMFADevice(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to enable MFA: %w", err)
	}

	log.Printf("Successfully enabled MFA for user: %s", username)
	return nil
}

func (m *MFAEnforcer) CreateMFAEnforcementPolicy() string {
	return `{
		"Version": "2012-10-17",
		"Statement": [{
			"Sid": "DenyAllExceptListedIfNoMFA",
			"Effect": "Deny",
			"NotAction": [
				"iam:CreateVirtualMFADevice",
				"iam:EnableMFADevice",
				"iam:GetUser",
				"iam:ListMFADevices",
				"iam:ListVirtualMFADevices",
				"iam:ResyncMFADevice",
				"sts:GetSessionToken"
			],
			"Resource": "*",
			"Condition": {
				"BoolIfExists": {"aws:MultiFactorAuthPresent": "false"}
			}
		}]
	}`
}

func strPtr(s string) *string { return &s }

func main() {
	enforcer, err := NewMFAEnforcer("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	policy := enforcer.CreateMFAEnforcementPolicy()
	fmt.Printf("MFA Enforcement Policy:\n%s\n", policy)
}
