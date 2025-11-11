package main

import (
	"fmt"
	"log"
	"math/rand"
	"sync"
)

type Backend struct {
	URL    string
	Healthy bool
	Weight  int
}

type LoadBalancer struct {
	backends []*Backend
	current  int
	mu       sync.Mutex
}

func NewLoadBalancer() *LoadBalancer {
	return &LoadBalancer{
		backends: make([]*Backend, 0),
		current:  0,
	}
}

func (lb *LoadBalancer) AddBackend(backend *Backend) {
	lb.mu.Lock()
	defer lb.mu.Unlock()
	lb.backends = append(lb.backends, backend)
}

func (lb *LoadBalancer) RoundRobin() *Backend {
	lb.mu.Lock()
	defer lb.mu.Unlock()
	
	if len(lb.backends) == 0 {
		return nil
	}
	
	backend := lb.backends[lb.current]
	lb.current = (lb.current + 1) % len(lb.backends)
	
	return backend
}

func (lb *LoadBalancer) LeastConnections() *Backend {
	lb.mu.Lock()
	defer lb.mu.Unlock()
	
	if len(lb.backends) == 0 {
		return nil
	}
	
	// Simplified - return random healthy backend
	for _, backend := range lb.backends {
		if backend.Healthy {
			return backend
		}
	}
	
	return nil
}

func (lb *LoadBalancer) WeightedRoundRobin() *Backend {
	lb.mu.Lock()
	defer lb.mu.Unlock()
	
	totalWeight := 0
	for _, backend := range lb.backends {
		if backend.Healthy {
			totalWeight += backend.Weight
		}
	}
	
	if totalWeight == 0 {
		return nil
	}
	
	random := rand.Intn(totalWeight)
	for _, backend := range lb.backends {
		if backend.Healthy {
			random -= backend.Weight
			if random < 0 {
				return backend
			}
		}
	}
	
	return nil
}

func (lb *LoadBalancer) HealthCheck() {
	lb.mu.Lock()
	defer lb.mu.Unlock()
	
	for _, backend := range lb.backends {
		backend.Healthy = lb.checkHealth(backend)
		status := "✅"
		if !backend.Healthy {
			status = "❌"
		}
		log.Printf("%s Backend: %s", status, backend.URL)
	}
}

func (lb *LoadBalancer) checkHealth(backend *Backend) bool {
	// Mock health check
	return true
}

func main() {
	lb := NewLoadBalancer()
	
	lb.AddBackend(&Backend{URL: "http://server1:8080", Healthy: true, Weight: 3})
	lb.AddBackend(&Backend{URL: "http://server2:8080", Healthy: true, Weight: 2})
	lb.AddBackend(&Backend{URL: "http://server3:8080", Healthy: true, Weight: 1})
	
	log.Println("⚖️  Load Balancer started")
	
	lb.HealthCheck()
	
	for i := 0; i < 10; i++ {
		backend := lb.RoundRobin()
		fmt.Printf("Request %d -> %s\n", i+1, backend.URL)
	}
}
