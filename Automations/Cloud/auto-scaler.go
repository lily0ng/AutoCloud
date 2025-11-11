package main

import (
	"context"
	"log"
	"time"
)

type AutoScaler struct {
	minInstances int
	maxInstances int
	current      int
	targetCPU    float64
}

func NewAutoScaler(min, max int, targetCPU float64) *AutoScaler {
	return &AutoScaler{
		minInstances: min,
		maxInstances: max,
		current:      min,
		targetCPU:    targetCPU,
	}
}

func (as *AutoScaler) Monitor(ctx context.Context) {
	ticker := time.NewTicker(30 * time.Second)
	defer ticker.Stop()
	
	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			as.checkAndScale()
		}
	}
}

func (as *AutoScaler) checkAndScale() {
	cpuUsage := as.getCurrentCPUUsage()
	
	log.Printf("Current CPU usage: %.2f%%, Instances: %d", cpuUsage, as.current)
	
	if cpuUsage > as.targetCPU+10 && as.current < as.maxInstances {
		as.scaleUp()
	} else if cpuUsage < as.targetCPU-10 && as.current > as.minInstances {
		as.scaleDown()
	}
}

func (as *AutoScaler) scaleUp() {
	as.current++
	log.Printf("⬆️  Scaling UP to %d instances", as.current)
	// Add instance logic here
}

func (as *AutoScaler) scaleDown() {
	as.current--
	log.Printf("⬇️  Scaling DOWN to %d instances", as.current)
	// Remove instance logic here
}

func (as *AutoScaler) getCurrentCPUUsage() float64 {
	// Mock CPU usage
	return 75.0
}

func main() {
	scaler := NewAutoScaler(2, 10, 70.0)
	
	ctx := context.Background()
	log.Println("🔄 Auto-scaler started")
	scaler.Monitor(ctx)
}
