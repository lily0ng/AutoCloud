package main

import (
	"context"
	"fmt"
	"log"
)

type VMConfig struct {
	Name         string
	InstanceType string
	ImageID      string
	Region       string
	VolumeSize   int
	Tags         map[string]string
}

type VMProvisioner struct {
	instances map[string]*VMInstance
}

type VMInstance struct {
	ID       string
	Config   VMConfig
	State    string
	PublicIP string
}

func NewVMProvisioner() *VMProvisioner {
	return &VMProvisioner{
		instances: make(map[string]*VMInstance),
	}
}

func (vp *VMProvisioner) ProvisionVM(ctx context.Context, config VMConfig) (*VMInstance, error) {
	log.Printf("🖥️  Provisioning VM: %s", config.Name)
	
	instance := &VMInstance{
		ID:       fmt.Sprintf("i-%d", len(vp.instances)+1),
		Config:   config,
		State:    "running",
		PublicIP: fmt.Sprintf("10.0.%d.%d", len(vp.instances), len(vp.instances)),
	}
	
	vp.instances[instance.ID] = instance
	log.Printf("✅ VM provisioned: %s (%s)", instance.ID, instance.PublicIP)
	
	return instance, nil
}

func (vp *VMProvisioner) TerminateVM(instanceID string) error {
	if _, exists := vp.instances[instanceID]; !exists {
		return fmt.Errorf("instance not found: %s", instanceID)
	}
	
	delete(vp.instances, instanceID)
	log.Printf("🗑️  VM terminated: %s", instanceID)
	return nil
}

func (vp *VMProvisioner) ListInstances() []*VMInstance {
	instances := make([]*VMInstance, 0, len(vp.instances))
	for _, instance := range vp.instances {
		instances = append(instances, instance)
	}
	return instances
}

func main() {
	provisioner := NewVMProvisioner()
	
	config := VMConfig{
		Name:         "web-server-1",
		InstanceType: "t3.medium",
		ImageID:      "ami-12345678",
		Region:       "us-east-1",
		VolumeSize:   50,
		Tags:         map[string]string{"Environment": "production"},
	}
	
	ctx := context.Background()
	instance, _ := provisioner.ProvisionVM(ctx, config)
	
	fmt.Printf("\n📊 Provisioned Instance:\n")
	fmt.Printf("  ID: %s\n", instance.ID)
	fmt.Printf("  IP: %s\n", instance.PublicIP)
	fmt.Printf("  State: %s\n", instance.State)
}
