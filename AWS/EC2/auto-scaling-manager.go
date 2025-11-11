package main

import (
	"fmt"
	"log"
	"time"
)

type AutoScalingGroup struct {
	Name         string
	MinSize      int
	MaxSize      int
	DesiredSize  int
	InstanceType string
	LaunchConfig string
}

type ScalingPolicy struct {
	Name       string
	MetricName string
	Threshold  float64
	ScaleUp    int
	ScaleDown  int
}

type EC2AutoScalingManager struct {
	groups   map[string]*AutoScalingGroup
	policies map[string]*ScalingPolicy
}

func NewAutoScalingManager() *EC2AutoScalingManager {
	return &EC2AutoScalingManager{
		groups:   make(map[string]*AutoScalingGroup),
		policies: make(map[string]*ScalingPolicy),
	}
}

func (asm *EC2AutoScalingManager) CreateAutoScalingGroup(asg *AutoScalingGroup) error {
	asm.groups[asg.Name] = asg
	log.Printf("📈 Auto Scaling Group created: %s (min: %d, max: %d, desired: %d)",
		asg.Name, asg.MinSize, asg.MaxSize, asg.DesiredSize)
	return nil
}

func (asm *EC2AutoScalingManager) AttachScalingPolicy(groupName string, policy *ScalingPolicy) error {
	if _, exists := asm.groups[groupName]; !exists {
		return fmt.Errorf("auto scaling group not found: %s", groupName)
	}
	
	asm.policies[policy.Name] = policy
	log.Printf("📊 Scaling policy attached: %s (metric: %s, threshold: %.2f)",
		policy.Name, policy.MetricName, policy.Threshold)
	return nil
}

func (asm *EC2AutoScalingManager) ScaleOut(groupName string, count int) error {
	group, exists := asm.groups[groupName]
	if !exists {
		return fmt.Errorf("group not found: %s", groupName)
	}
	
	newSize := group.DesiredSize + count
	if newSize > group.MaxSize {
		newSize = group.MaxSize
	}
	
	group.DesiredSize = newSize
	log.Printf("⬆️  Scaling out %s: %d instances (new desired: %d)", groupName, count, newSize)
	return nil
}

func (asm *EC2AutoScalingManager) ScaleIn(groupName string, count int) error {
	group, exists := asm.groups[groupName]
	if !exists {
		return fmt.Errorf("group not found: %s", groupName)
	}
	
	newSize := group.DesiredSize - count
	if newSize < group.MinSize {
		newSize = group.MinSize
	}
	
	group.DesiredSize = newSize
	log.Printf("⬇️  Scaling in %s: %d instances (new desired: %d)", groupName, count, newSize)
	return nil
}

func (asm *EC2AutoScalingManager) MonitorAndScale(groupName string) {
	ticker := time.NewTicker(30 * time.Second)
	defer ticker.Stop()
	
	for range ticker.C {
		// Simulate metric check
		cpuUsage := 75.0 // Mock CPU usage
		
		for _, policy := range asm.policies {
			if policy.MetricName == "CPUUtilization" {
				if cpuUsage > policy.Threshold {
					asm.ScaleOut(groupName, policy.ScaleUp)
				} else if cpuUsage < policy.Threshold-20 {
					asm.ScaleIn(groupName, policy.ScaleDown)
				}
			}
		}
	}
}

func main() {
	manager := NewAutoScalingManager()
	
	// Create Auto Scaling Group
	asg := &AutoScalingGroup{
		Name:         "web-servers-asg",
		MinSize:      2,
		MaxSize:      10,
		DesiredSize:  3,
		InstanceType: "t3.medium",
		LaunchConfig: "web-server-lc-v1",
	}
	manager.CreateAutoScalingGroup(asg)
	
	// Attach Scaling Policy
	policy := &ScalingPolicy{
		Name:       "cpu-scale-policy",
		MetricName: "CPUUtilization",
		Threshold:  70.0,
		ScaleUp:    2,
		ScaleDown:  1,
	}
	manager.AttachScalingPolicy("web-servers-asg", policy)
	
	fmt.Println("✅ Auto Scaling configured")
}
