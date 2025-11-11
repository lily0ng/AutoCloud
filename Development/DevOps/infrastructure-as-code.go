package main

import (
	"fmt"
	"log"
)

type Resource struct {
	Type       string
	Name       string
	Properties map[string]interface{}
	DependsOn  []string
}

type Stack struct {
	Name      string
	Resources []Resource
	Outputs   map[string]string
}

type IaCEngine struct {
	stacks map[string]*Stack
}

func NewIaCEngine() *IaCEngine {
	return &IaCEngine{
		stacks: make(map[string]*Stack),
	}
}

func (iac *IaCEngine) CreateStack(name string) *Stack {
	stack := &Stack{
		Name:      name,
		Resources: make([]Resource, 0),
		Outputs:   make(map[string]string),
	}
	iac.stacks[name] = stack
	log.Printf("📦 Stack created: %s", name)
	return stack
}

func (iac *IaCEngine) AddResource(stackName string, resource Resource) error {
	stack, exists := iac.stacks[stackName]
	if !exists {
		return fmt.Errorf("stack not found: %s", stackName)
	}
	
	stack.Resources = append(stack.Resources, resource)
	log.Printf("➕ Resource added to %s: %s (%s)", stackName, resource.Name, resource.Type)
	return nil
}

func (iac *IaCEngine) DeployStack(stackName string) error {
	stack, exists := iac.stacks[stackName]
	if !exists {
		return fmt.Errorf("stack not found: %s", stackName)
	}
	
	log.Printf("🚀 Deploying stack: %s", stackName)
	log.Printf("   Resources: %d", len(stack.Resources))
	
	for i, resource := range stack.Resources {
		log.Printf("   [%d/%d] Creating %s: %s", i+1, len(stack.Resources), resource.Type, resource.Name)
	}
	
	log.Printf("✅ Stack deployed: %s", stackName)
	return nil
}

func (iac *IaCEngine) UpdateStack(stackName string) error {
	stack, exists := iac.stacks[stackName]
	if !exists {
		return fmt.Errorf("stack not found: %s", stackName)
	}
	
	log.Printf("🔄 Updating stack: %s", stackName)
	log.Printf("   Calculating changes...")
	log.Printf("   Resources to update: 2")
	log.Printf("   Resources to add: 1")
	log.Printf("   Resources to remove: 0")
	log.Printf("✅ Stack updated: %s", stackName)
	return nil
}

func (iac *IaCEngine) DestroyStack(stackName string) error {
	stack, exists := iac.stacks[stackName]
	if !exists {
		return fmt.Errorf("stack not found: %s", stackName)
	}
	
	log.Printf("🗑️  Destroying stack: %s", stackName)
	
	for i := len(stack.Resources) - 1; i >= 0; i-- {
		resource := stack.Resources[i]
		log.Printf("   Deleting %s: %s", resource.Type, resource.Name)
	}
	
	delete(iac.stacks, stackName)
	log.Printf("✅ Stack destroyed: %s", stackName)
	return nil
}

func main() {
	engine := NewIaCEngine()
	
	// Create infrastructure stack
	stack := engine.CreateStack("web-infrastructure")
	
	// Add VPC
	engine.AddResource("web-infrastructure", Resource{
		Type: "AWS::EC2::VPC",
		Name: "main-vpc",
		Properties: map[string]interface{}{
			"CidrBlock": "10.0.0.0/16",
			"Tags":      map[string]string{"Name": "main-vpc"},
		},
	})
	
	// Add Subnet
	engine.AddResource("web-infrastructure", Resource{
		Type: "AWS::EC2::Subnet",
		Name: "public-subnet",
		Properties: map[string]interface{}{
			"VpcId":     "${main-vpc.id}",
			"CidrBlock": "10.0.1.0/24",
		},
		DependsOn: []string{"main-vpc"},
	})
	
	// Add Security Group
	engine.AddResource("web-infrastructure", Resource{
		Type: "AWS::EC2::SecurityGroup",
		Name: "web-sg",
		Properties: map[string]interface{}{
			"VpcId":       "${main-vpc.id}",
			"Description": "Web server security group",
			"IngressRules": []map[string]interface{}{
				{"Port": 80, "Protocol": "tcp", "CidrIp": "0.0.0.0/0"},
				{"Port": 443, "Protocol": "tcp", "CidrIp": "0.0.0.0/0"},
			},
		},
		DependsOn: []string{"main-vpc"},
	})
	
	// Add EC2 Instance
	engine.AddResource("web-infrastructure", Resource{
		Type: "AWS::EC2::Instance",
		Name: "web-server",
		Properties: map[string]interface{}{
			"InstanceType": "t3.medium",
			"ImageId":      "ami-12345678",
			"SubnetId":     "${public-subnet.id}",
			"SecurityGroups": []string{"${web-sg.id}"},
		},
		DependsOn: []string{"public-subnet", "web-sg"},
	})
	
	// Deploy stack
	engine.DeployStack("web-infrastructure")
	
	// Update stack
	engine.UpdateStack("web-infrastructure")
	
	fmt.Println("\n✅ Infrastructure as Code complete")
}
