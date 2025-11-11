package main

import (
	"fmt"
	"log"
)

type Container struct {
	ID      string
	Image   string
	Name    string
	Status  string
	Ports   []string
	Volumes []string
}

type ContainerRuntime struct {
	containers map[string]*Container
}

func NewContainerRuntime() *ContainerRuntime {
	return &ContainerRuntime{
		containers: make(map[string]*Container),
	}
}

func (cr *ContainerRuntime) RunContainer(image, name string, ports, volumes []string) (*Container, error) {
	container := &Container{
		ID:      fmt.Sprintf("container-%d", len(cr.containers)+1),
		Image:   image,
		Name:    name,
		Status:  "running",
		Ports:   ports,
		Volumes: volumes,
	}
	
	cr.containers[container.ID] = container
	log.Printf("🐳 Container started: %s (%s)", name, container.ID)
	
	return container, nil
}

func (cr *ContainerRuntime) StopContainer(containerID string) error {
	container, exists := cr.containers[containerID]
	if !exists {
		return fmt.Errorf("container not found: %s", containerID)
	}
	
	container.Status = "stopped"
	log.Printf("⏹️  Container stopped: %s", containerID)
	return nil
}

func (cr *ContainerRuntime) RemoveContainer(containerID string) error {
	delete(cr.containers, containerID)
	log.Printf("🗑️  Container removed: %s", containerID)
	return nil
}

func (cr *ContainerRuntime) ListContainers() []*Container {
	containers := make([]*Container, 0, len(cr.containers))
	for _, c := range cr.containers {
		containers = append(containers, c)
	}
	return containers
}

func main() {
	runtime := NewContainerRuntime()
	
	runtime.RunContainer("nginx:latest", "web-server", []string{"80:80"}, []string{"/data:/var/www"})
	runtime.RunContainer("postgres:14", "database", []string{"5432:5432"}, []string{"/db:/var/lib/postgresql"})
	
	fmt.Println("\n📦 Running Containers:")
	for _, c := range runtime.ListContainers() {
		fmt.Printf("  %s: %s (%s)\n", c.Name, c.Image, c.Status)
	}
}
