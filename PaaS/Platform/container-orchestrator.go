package main

import (
	"fmt"
	"log"
	"time"
)

type ContainerSpec struct {
	Image       string
	Name        string
	Replicas    int
	CPU         string
	Memory      string
	Environment map[string]string
	Ports       []int
}

type Deployment struct {
	Name      string
	Namespace string
	Spec      ContainerSpec
	Status    string
	CreatedAt time.Time
}

type ContainerOrchestrator struct {
	deployments map[string]*Deployment
	pods        map[string][]string
}

func NewContainerOrchestrator() *ContainerOrchestrator {
	return &ContainerOrchestrator{
		deployments: make(map[string]*Deployment),
		pods:        make(map[string][]string),
	}
}

func (co *ContainerOrchestrator) Deploy(spec ContainerSpec, namespace string) (*Deployment, error) {
	deployment := &Deployment{
		Name:      spec.Name,
		Namespace: namespace,
		Spec:      spec,
		Status:    "Running",
		CreatedAt: time.Now(),
	}
	
	co.deployments[spec.Name] = deployment
	
	// Create pods
	pods := make([]string, spec.Replicas)
	for i := 0; i < spec.Replicas; i++ {
		podName := fmt.Sprintf("%s-%d", spec.Name, i)
		pods[i] = podName
	}
	co.pods[spec.Name] = pods
	
	log.Printf("🚀 Deployment created: %s in namespace %s", spec.Name, namespace)
	log.Printf("   Image: %s", spec.Image)
	log.Printf("   Replicas: %d", spec.Replicas)
	log.Printf("   Resources: CPU=%s, Memory=%s", spec.CPU, spec.Memory)
	
	return deployment, nil
}

func (co *ContainerOrchestrator) Scale(deploymentName string, replicas int) error {
	deployment, exists := co.deployments[deploymentName]
	if !exists {
		return fmt.Errorf("deployment not found: %s", deploymentName)
	}
	
	oldReplicas := deployment.Spec.Replicas
	deployment.Spec.Replicas = replicas
	
	// Update pods
	pods := make([]string, replicas)
	for i := 0; i < replicas; i++ {
		podName := fmt.Sprintf("%s-%d", deploymentName, i)
		pods[i] = podName
	}
	co.pods[deploymentName] = pods
	
	log.Printf("📈 Scaled %s: %d -> %d replicas", deploymentName, oldReplicas, replicas)
	return nil
}

func (co *ContainerOrchestrator) RollingUpdate(deploymentName, newImage string) error {
	deployment, exists := co.deployments[deploymentName]
	if !exists {
		return fmt.Errorf("deployment not found: %s", deploymentName)
	}
	
	oldImage := deployment.Spec.Image
	deployment.Spec.Image = newImage
	
	log.Printf("🔄 Rolling update for %s:", deploymentName)
	log.Printf("   Old image: %s", oldImage)
	log.Printf("   New image: %s", newImage)
	
	// Simulate rolling update
	for i, pod := range co.pods[deploymentName] {
		log.Printf("   Updating pod %d/%d: %s", i+1, len(co.pods[deploymentName]), pod)
		time.Sleep(100 * time.Millisecond)
	}
	
	log.Printf("✅ Rolling update complete")
	return nil
}

func (co *ContainerOrchestrator) GetStatus(deploymentName string) {
	deployment, exists := co.deployments[deploymentName]
	if !exists {
		log.Printf("❌ Deployment not found: %s", deploymentName)
		return
	}
	
	fmt.Printf("\n📊 Deployment Status: %s\n", deploymentName)
	fmt.Printf("   Namespace: %s\n", deployment.Namespace)
	fmt.Printf("   Status: %s\n", deployment.Status)
	fmt.Printf("   Replicas: %d\n", deployment.Spec.Replicas)
	fmt.Printf("   Image: %s\n", deployment.Spec.Image)
	fmt.Printf("   Created: %s\n", deployment.CreatedAt.Format(time.RFC3339))
	fmt.Printf("   Pods:\n")
	for _, pod := range co.pods[deploymentName] {
		fmt.Printf("     - %s (Running)\n", pod)
	}
}

func main() {
	orchestrator := NewContainerOrchestrator()
	
	// Deploy application
	spec := ContainerSpec{
		Image:    "nginx:1.21",
		Name:     "web-app",
		Replicas: 3,
		CPU:      "500m",
		Memory:   "512Mi",
		Environment: map[string]string{
			"ENV":      "production",
			"LOG_LEVEL": "info",
		},
		Ports: []int{80, 443},
	}
	
	orchestrator.Deploy(spec, "production")
	
	// Scale deployment
	orchestrator.Scale("web-app", 5)
	
	// Rolling update
	orchestrator.RollingUpdate("web-app", "nginx:1.22")
	
	// Get status
	orchestrator.GetStatus("web-app")
	
	fmt.Println("\n✅ Container orchestration complete")
}
