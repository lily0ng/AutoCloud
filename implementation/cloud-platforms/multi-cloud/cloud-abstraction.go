package main

import (
	"fmt"
	"log"
)

// CloudProvider interface for multi-cloud abstraction
type CloudProvider interface {
	CreateInstance(config InstanceConfig) (string, error)
	DeleteInstance(instanceID string) error
	ListInstances() ([]Instance, error)
	GetInstanceStatus(instanceID string) (string, error)
}

type InstanceConfig struct {
	Name         string
	InstanceType string
	Region       string
	ImageID      string
}

type Instance struct {
	ID       string
	Name     string
	Type     string
	Status   string
	Provider string
}

// AWS Provider
type AWSProvider struct {
	Region string
}

func (a *AWSProvider) CreateInstance(config InstanceConfig) (string, error) {
	log.Printf("Creating AWS instance: %s", config.Name)
	// AWS-specific implementation
	return "aws-instance-123", nil
}

func (a *AWSProvider) DeleteInstance(instanceID string) error {
	log.Printf("Deleting AWS instance: %s", instanceID)
	return nil
}

func (a *AWSProvider) ListInstances() ([]Instance, error) {
	return []Instance{
		{ID: "aws-1", Name: "aws-instance-1", Type: "t3.micro", Status: "running", Provider: "AWS"},
	}, nil
}

func (a *AWSProvider) GetInstanceStatus(instanceID string) (string, error) {
	return "running", nil
}

// Azure Provider
type AzureProvider struct {
	SubscriptionID string
}

func (az *AzureProvider) CreateInstance(config InstanceConfig) (string, error) {
	log.Printf("Creating Azure VM: %s", config.Name)
	// Azure-specific implementation
	return "azure-vm-123", nil
}

func (az *AzureProvider) DeleteInstance(instanceID string) error {
	log.Printf("Deleting Azure VM: %s", instanceID)
	return nil
}

func (az *AzureProvider) ListInstances() ([]Instance, error) {
	return []Instance{
		{ID: "azure-1", Name: "azure-vm-1", Type: "Standard_B2s", Status: "running", Provider: "Azure"},
	}, nil
}

func (az *AzureProvider) GetInstanceStatus(instanceID string) (string, error) {
	return "running", nil
}

// GCP Provider
type GCPProvider struct {
	ProjectID string
}

func (g *GCPProvider) CreateInstance(config InstanceConfig) (string, error) {
	log.Printf("Creating GCP instance: %s", config.Name)
	// GCP-specific implementation
	return "gcp-instance-123", nil
}

func (g *GCPProvider) DeleteInstance(instanceID string) error {
	log.Printf("Deleting GCP instance: %s", instanceID)
	return nil
}

func (g *GCPProvider) ListInstances() ([]Instance, error) {
	return []Instance{
		{ID: "gcp-1", Name: "gcp-instance-1", Type: "e2-medium", Status: "running", Provider: "GCP"},
	}, nil
}

func (g *GCPProvider) GetInstanceStatus(instanceID string) (string, error) {
	return "running", nil
}

// Multi-Cloud Manager
type MultiCloudManager struct {
	providers map[string]CloudProvider
}

func NewMultiCloudManager() *MultiCloudManager {
	return &MultiCloudManager{
		providers: make(map[string]CloudProvider),
	}
}

func (m *MultiCloudManager) RegisterProvider(name string, provider CloudProvider) {
	m.providers[name] = provider
	log.Printf("Registered provider: %s", name)
}

func (m *MultiCloudManager) CreateInstanceOnProvider(providerName string, config InstanceConfig) (string, error) {
	provider, exists := m.providers[providerName]
	if !exists {
		return "", fmt.Errorf("provider %s not found", providerName)
	}
	return provider.CreateInstance(config)
}

func (m *MultiCloudManager) ListAllInstances() ([]Instance, error) {
	var allInstances []Instance
	for _, provider := range m.providers {
		instances, err := provider.ListInstances()
		if err != nil {
			return nil, err
		}
		allInstances = append(allInstances, instances...)
	}
	return allInstances, nil
}

func main() {
	manager := NewMultiCloudManager()
	
	// Register providers
	manager.RegisterProvider("aws", &AWSProvider{Region: "us-east-1"})
	manager.RegisterProvider("azure", &AzureProvider{SubscriptionID: "sub-123"})
	manager.RegisterProvider("gcp", &GCPProvider{ProjectID: "project-123"})
	
	// List all instances across clouds
	instances, _ := manager.ListAllInstances()
	fmt.Println("All instances across clouds:")
	for _, inst := range instances {
		fmt.Printf("  %s: %s (%s) - %s\n", inst.Provider, inst.Name, inst.Type, inst.Status)
	}
}
