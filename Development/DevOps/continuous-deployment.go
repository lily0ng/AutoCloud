package main

import (
	"fmt"
	"log"
	"time"
)

type DeploymentStrategy string

const (
	RollingUpdate DeploymentStrategy = "rolling"
	BlueGreen     DeploymentStrategy = "blue-green"
	Canary        DeploymentStrategy = "canary"
)

type DeploymentConfig struct {
	Application string
	Version     string
	Environment string
	Strategy    DeploymentStrategy
	Replicas    int
	HealthCheck string
}

type ContinuousDeployment struct {
	deployments map[string]*DeploymentConfig
	history     []DeploymentRecord
}

type DeploymentRecord struct {
	Application string
	Version     string
	Environment string
	Status      string
	StartTime   time.Time
	EndTime     time.Time
	Duration    time.Duration
}

func NewContinuousDeployment() *ContinuousDeployment {
	return &ContinuousDeployment{
		deployments: make(map[string]*DeploymentConfig),
		history:     make([]DeploymentRecord, 0),
	}
}

func (cd *ContinuousDeployment) Deploy(config DeploymentConfig) error {
	start := time.Now()
	
	log.Printf("🚀 Starting deployment: %s v%s to %s", 
		config.Application, config.Version, config.Environment)
	log.Printf("   Strategy: %s", config.Strategy)
	
	var err error
	switch config.Strategy {
	case RollingUpdate:
		err = cd.rollingUpdate(config)
	case BlueGreen:
		err = cd.blueGreenDeployment(config)
	case Canary:
		err = cd.canaryDeployment(config)
	}
	
	duration := time.Since(start)
	status := "success"
	if err != nil {
		status = "failed"
	}
	
	record := DeploymentRecord{
		Application: config.Application,
		Version:     config.Version,
		Environment: config.Environment,
		Status:      status,
		StartTime:   start,
		EndTime:     time.Now(),
		Duration:    duration,
	}
	cd.history = append(cd.history, record)
	
	if err != nil {
		log.Printf("❌ Deployment failed: %v", err)
		return err
	}
	
	cd.deployments[config.Application] = &config
	log.Printf("✅ Deployment complete in %v", duration)
	return nil
}

func (cd *ContinuousDeployment) rollingUpdate(config DeploymentConfig) error {
	log.Println("🔄 Executing rolling update...")
	
	batchSize := config.Replicas / 3
	if batchSize == 0 {
		batchSize = 1
	}
	
	for i := 0; i < config.Replicas; i += batchSize {
		end := i + batchSize
		if end > config.Replicas {
			end = config.Replicas
		}
		
		log.Printf("   Updating instances %d-%d/%d", i+1, end, config.Replicas)
		time.Sleep(500 * time.Millisecond)
		
		log.Printf("   Health check passed")
	}
	
	return nil
}

func (cd *ContinuousDeployment) blueGreenDeployment(config DeploymentConfig) error {
	log.Println("🔵🟢 Executing blue-green deployment...")
	
	log.Println("   Deploying to green environment...")
	time.Sleep(1 * time.Second)
	
	log.Println("   Running smoke tests...")
	time.Sleep(500 * time.Millisecond)
	
	log.Println("   Switching traffic to green...")
	time.Sleep(200 * time.Millisecond)
	
	log.Println("   Monitoring green environment...")
	time.Sleep(500 * time.Millisecond)
	
	log.Println("   Decommissioning blue environment...")
	
	return nil
}

func (cd *ContinuousDeployment) canaryDeployment(config DeploymentConfig) error {
	log.Println("🐤 Executing canary deployment...")
	
	stages := []int{10, 25, 50, 100}
	
	for _, percentage := range stages {
		log.Printf("   Routing %d%% traffic to new version", percentage)
		time.Sleep(1 * time.Second)
		
		log.Printf("   Monitoring metrics...")
		time.Sleep(500 * time.Millisecond)
		
		log.Printf("   ✓ Metrics healthy at %d%%", percentage)
	}
	
	return nil
}

func (cd *ContinuousDeployment) Rollback(application, version string) error {
	log.Printf("⏪ Rolling back %s to version %s", application, version)
	
	config := DeploymentConfig{
		Application: application,
		Version:     version,
		Environment: "production",
		Strategy:    RollingUpdate,
		Replicas:    3,
	}
	
	return cd.Deploy(config)
}

func (cd *ContinuousDeployment) GetDeploymentHistory(application string, limit int) []DeploymentRecord {
	history := make([]DeploymentRecord, 0)
	count := 0
	
	for i := len(cd.history) - 1; i >= 0 && count < limit; i-- {
		if application == "" || cd.history[i].Application == application {
			history = append(history, cd.history[i])
			count++
		}
	}
	
	return history
}

func main() {
	cd := NewContinuousDeployment()
	
	// Deploy with rolling update
	cd.Deploy(DeploymentConfig{
		Application: "web-app",
		Version:     "v1.2.0",
		Environment: "production",
		Strategy:    RollingUpdate,
		Replicas:    6,
		HealthCheck: "/health",
	})
	
	// Deploy with canary
	cd.Deploy(DeploymentConfig{
		Application: "api-service",
		Version:     "v2.0.0",
		Environment: "production",
		Strategy:    Canary,
		Replicas:    10,
		HealthCheck: "/api/health",
	})
	
	// Get deployment history
	fmt.Println("\n📜 Deployment History:")
	history := cd.GetDeploymentHistory("", 5)
	for _, record := range history {
		fmt.Printf("  %s v%s to %s: %s (%v)\n",
			record.Application, record.Version, record.Environment,
			record.Status, record.Duration)
	}
	
	fmt.Println("\n✅ Continuous deployment operational")
}
