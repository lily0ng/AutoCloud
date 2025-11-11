package main

import (
	"fmt"
	"log"
	"sync"
	"time"
)

type ServiceInstance struct {
	ID       string
	Name     string
	Host     string
	Port     int
	Health   string
	Metadata map[string]string
	LastSeen time.Time
}

type ServiceRegistry struct {
	services map[string][]*ServiceInstance
	mu       sync.RWMutex
	ttl      time.Duration
}

func NewServiceRegistry(ttl time.Duration) *ServiceRegistry {
	sr := &ServiceRegistry{
		services: make(map[string][]*ServiceInstance),
		ttl:      ttl,
	}
	go sr.cleanupStaleServices()
	return sr
}

func (sr *ServiceRegistry) Register(instance *ServiceInstance) error {
	sr.mu.Lock()
	defer sr.mu.Unlock()
	
	instance.LastSeen = time.Now()
	instance.Health = "healthy"
	
	instances := sr.services[instance.Name]
	
	// Check if instance already exists
	found := false
	for i, existing := range instances {
		if existing.ID == instance.ID {
			instances[i] = instance
			found = true
			break
		}
	}
	
	if !found {
		instances = append(instances, instance)
	}
	
	sr.services[instance.Name] = instances
	
	log.Printf("✅ Service registered: %s (%s:%d)", instance.Name, instance.Host, instance.Port)
	return nil
}

func (sr *ServiceRegistry) Deregister(serviceName, instanceID string) error {
	sr.mu.Lock()
	defer sr.mu.Unlock()
	
	instances := sr.services[serviceName]
	newInstances := make([]*ServiceInstance, 0)
	
	for _, instance := range instances {
		if instance.ID != instanceID {
			newInstances = append(newInstances, instance)
		}
	}
	
	sr.services[serviceName] = newInstances
	log.Printf("🗑️  Service deregistered: %s (%s)", serviceName, instanceID)
	return nil
}

func (sr *ServiceRegistry) Discover(serviceName string) ([]*ServiceInstance, error) {
	sr.mu.RLock()
	defer sr.mu.RUnlock()
	
	instances, exists := sr.services[serviceName]
	if !exists || len(instances) == 0 {
		return nil, fmt.Errorf("service not found: %s", serviceName)
	}
	
	// Filter healthy instances
	healthy := make([]*ServiceInstance, 0)
	for _, instance := range instances {
		if instance.Health == "healthy" {
			healthy = append(healthy, instance)
		}
	}
	
	return healthy, nil
}

func (sr *ServiceRegistry) Heartbeat(serviceName, instanceID string) error {
	sr.mu.Lock()
	defer sr.mu.Unlock()
	
	instances := sr.services[serviceName]
	for _, instance := range instances {
		if instance.ID == instanceID {
			instance.LastSeen = time.Now()
			instance.Health = "healthy"
			return nil
		}
	}
	
	return fmt.Errorf("instance not found: %s/%s", serviceName, instanceID)
}

func (sr *ServiceRegistry) cleanupStaleServices() {
	ticker := time.NewTicker(30 * time.Second)
	defer ticker.Stop()
	
	for range ticker.C {
		sr.mu.Lock()
		
		for serviceName, instances := range sr.services {
			activeInstances := make([]*ServiceInstance, 0)
			
			for _, instance := range instances {
				if time.Since(instance.LastSeen) < sr.ttl {
					activeInstances = append(activeInstances, instance)
				} else {
					log.Printf("⚠️  Removing stale instance: %s (%s)", serviceName, instance.ID)
				}
			}
			
			sr.services[serviceName] = activeInstances
		}
		
		sr.mu.Unlock()
	}
}

func (sr *ServiceRegistry) GetAllServices() map[string][]*ServiceInstance {
	sr.mu.RLock()
	defer sr.mu.RUnlock()
	
	result := make(map[string][]*ServiceInstance)
	for name, instances := range sr.services {
		result[name] = instances
	}
	return result
}

func (sr *ServiceRegistry) GetServiceCount() int {
	sr.mu.RLock()
	defer sr.mu.RUnlock()
	return len(sr.services)
}

func main() {
	registry := NewServiceRegistry(60 * time.Second)
	
	// Register services
	registry.Register(&ServiceInstance{
		ID:   "user-service-1",
		Name: "user-service",
		Host: "10.0.1.10",
		Port: 8001,
		Metadata: map[string]string{
			"version": "v1.0.0",
			"region":  "us-east-1",
		},
	})
	
	registry.Register(&ServiceInstance{
		ID:   "user-service-2",
		Name: "user-service",
		Host: "10.0.1.11",
		Port: 8001,
		Metadata: map[string]string{
			"version": "v1.0.0",
			"region":  "us-east-1",
		},
	})
	
	registry.Register(&ServiceInstance{
		ID:   "order-service-1",
		Name: "order-service",
		Host: "10.0.2.10",
		Port: 8002,
		Metadata: map[string]string{
			"version": "v2.0.0",
			"region":  "us-west-2",
		},
	})
	
	// Discover services
	fmt.Println("\n🔍 Service Discovery:")
	userServices, _ := registry.Discover("user-service")
	fmt.Printf("   Found %d instances of user-service:\n", len(userServices))
	for _, instance := range userServices {
		fmt.Printf("     - %s (%s:%d) [%s]\n", instance.ID, instance.Host, instance.Port, instance.Health)
	}
	
	// Send heartbeat
	registry.Heartbeat("user-service", "user-service-1")
	
	// Get all services
	fmt.Println("\n📋 All Services:")
	allServices := registry.GetAllServices()
	for name, instances := range allServices {
		fmt.Printf("   %s: %d instances\n", name, len(instances))
	}
	
	fmt.Println("\n✅ Service discovery operational")
}
