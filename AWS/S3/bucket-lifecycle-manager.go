package main

import (
	"fmt"
	"log"
	"time"
)

type LifecycleRule struct {
	ID                   string
	Prefix               string
	Status               string
	TransitionDays       int
	TransitionClass      string
	ExpirationDays       int
	NoncurrentVersionExp int
}

type S3LifecycleManager struct {
	buckets map[string][]LifecycleRule
}

func NewS3LifecycleManager() *S3LifecycleManager {
	return &S3LifecycleManager{
		buckets: make(map[string][]LifecycleRule),
	}
}

func (lm *S3LifecycleManager) AddLifecycleRule(bucket string, rule LifecycleRule) error {
	lm.buckets[bucket] = append(lm.buckets[bucket], rule)
	log.Printf("📋 Lifecycle rule added to %s: %s", bucket, rule.ID)
	log.Printf("   Transition to %s after %d days", rule.TransitionClass, rule.TransitionDays)
	log.Printf("   Expiration after %d days", rule.ExpirationDays)
	return nil
}

func (lm *S3LifecycleManager) ApplyLifecycleRules(bucket string) error {
	rules, exists := lm.buckets[bucket]
	if !exists {
		return fmt.Errorf("no rules found for bucket: %s", bucket)
	}
	
	log.Printf("🔄 Applying %d lifecycle rules to %s", len(rules), bucket)
	for _, rule := range rules {
		log.Printf("   ✓ %s: %s", rule.ID, rule.Status)
	}
	return nil
}

func (lm *S3LifecycleManager) GetCostSavings(bucket string) float64 {
	rules, exists := lm.buckets[bucket]
	if !exists {
		return 0
	}
	
	// Mock calculation
	savings := float64(len(rules)) * 100.0
	log.Printf("💰 Estimated monthly savings for %s: $%.2f", bucket, savings)
	return savings
}

func main() {
	manager := NewS3LifecycleManager()
	
	// Add lifecycle rules
	manager.AddLifecycleRule("my-data-bucket", LifecycleRule{
		ID:              "archive-old-data",
		Prefix:          "logs/",
		Status:          "Enabled",
		TransitionDays:  30,
		TransitionClass: "GLACIER",
		ExpirationDays:  365,
	})
	
	manager.AddLifecycleRule("my-data-bucket", LifecycleRule{
		ID:              "delete-temp-files",
		Prefix:          "temp/",
		Status:          "Enabled",
		ExpirationDays:  7,
	})
	
	manager.ApplyLifecycleRules("my-data-bucket")
	manager.GetCostSavings("my-data-bucket")
	
	fmt.Println("✅ Lifecycle management configured")
}
