package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
)

type KeyPairManager struct {
	client *ec2.Client
	ctx    context.Context
}

func NewKeyPairManager(region string) (*KeyPairManager, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &KeyPairManager{
		client: ec2.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *KeyPairManager) CreateKeyPair(name string) (string, error) {
	input := &ec2.CreateKeyPairInput{
		KeyName: &name,
	}

	result, err := m.client.CreateKeyPair(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create key pair: %w", err)
	}

	privateKey := *result.KeyMaterial
	log.Printf("Successfully created key pair: %s", name)
	
	// Save private key to file
	filename := fmt.Sprintf("%s.pem", name)
	err = os.WriteFile(filename, []byte(privateKey), 0600)
	if err != nil {
		return "", fmt.Errorf("failed to save private key: %w", err)
	}

	return filename, nil
}

func (m *KeyPairManager) DeleteKeyPair(name string) error {
	input := &ec2.DeleteKeyPairInput{
		KeyName: &name,
	}

	_, err := m.client.DeleteKeyPair(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete key pair: %w", err)
	}

	log.Printf("Successfully deleted key pair: %s", name)
	return nil
}

func main() {
	manager, err := NewKeyPairManager("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	filename, err := manager.CreateKeyPair("autocloud-key")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Private key saved to: %s\n", filename)
}
