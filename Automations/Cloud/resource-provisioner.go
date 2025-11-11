package main

import (
	"context"
	"fmt"
	"log"
)

type ResourceType string

const (
	VM       ResourceType = "vm"
	Database ResourceType = "database"
	Storage  ResourceType = "storage"
	Network  ResourceType = "network"
)

type Resource struct {
	Type   ResourceType
	Name   string
	Config map[string]interface{}
}

type ResourceProvisioner struct {
	resources []Resource
}

func NewResourceProvisioner() *ResourceProvisioner {
	return &ResourceProvisioner{
		resources: make([]Resource, 0),
	}
}

func (rp *ResourceProvisioner) AddResource(resource Resource) {
	rp.resources = append(rp.resources, resource)
}

func (rp *ResourceProvisioner) Provision(ctx context.Context) error {
	for _, resource := range rp.resources {
		log.Printf("Provisioning %s: %s", resource.Type, resource.Name)
		
		switch resource.Type {
		case VM:
			if err := rp.provisionVM(ctx, resource); err != nil {
				return err
			}
		case Database:
			if err := rp.provisionDatabase(ctx, resource); err != nil {
				return err
			}
		case Storage:
			if err := rp.provisionStorage(ctx, resource); err != nil {
				return err
			}
		case Network:
			if err := rp.provisionNetwork(ctx, resource); err != nil {
				return err
			}
		}
	}
	
	log.Println("✅ All resources provisioned")
	return nil
}

func (rp *ResourceProvisioner) provisionVM(ctx context.Context, resource Resource) error {
	log.Printf("Creating VM: %s", resource.Name)
	return nil
}

func (rp *ResourceProvisioner) provisionDatabase(ctx context.Context, resource Resource) error {
	log.Printf("Creating database: %s", resource.Name)
	return nil
}

func (rp *ResourceProvisioner) provisionStorage(ctx context.Context, resource Resource) error {
	log.Printf("Creating storage: %s", resource.Name)
	return nil
}

func (rp *ResourceProvisioner) provisionNetwork(ctx context.Context, resource Resource) error {
	log.Printf("Creating network: %s", resource.Name)
	return nil
}

func main() {
	provisioner := NewResourceProvisioner()
	
	provisioner.AddResource(Resource{
		Type: VM,
		Name: "web-server-1",
		Config: map[string]interface{}{
			"instance_type": "t3.medium",
			"ami":           "ami-12345678",
		},
	})
	
	provisioner.AddResource(Resource{
		Type: Database,
		Name: "postgres-db",
		Config: map[string]interface{}{
			"engine":  "postgres",
			"version": "14",
		},
	})
	
	ctx := context.Background()
	if err := provisioner.Provision(ctx); err != nil {
		log.Fatal(err)
	}
}
