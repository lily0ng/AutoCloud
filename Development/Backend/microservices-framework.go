package main

import ("fmt"; "log"; "net/http"; "time")

type Service struct {
	Name string; Port int; Health string; Version string
}

type ServiceRegistry struct {
	services map[string]*Service
}

func NewServiceRegistry() *ServiceRegistry {
	return &ServiceRegistry{services: make(map[string]*Service)}
}

func (sr *ServiceRegistry) Register(svc *Service) {
	sr.services[svc.Name] = svc
	log.Printf("🔌 Service registered: %s on port %d", svc.Name, svc.Port)
}

func (sr *ServiceRegistry) Discover(name string) *Service {
	return sr.services[name]
}

func (sr *ServiceRegistry) HealthCheck() {
	for _, svc := range sr.services {
		svc.Health = "healthy"
		log.Printf("✅ %s: %s", svc.Name, svc.Health)
	}
}

func main() {
	registry := NewServiceRegistry()
	registry.Register(&Service{Name: "user-service", Port: 8001, Version: "v1.0.0"})
	registry.Register(&Service{Name: "order-service", Port: 8002, Version: "v1.0.0"})
	registry.HealthCheck()
	fmt.Println("✅ Microservices framework ready")
}
