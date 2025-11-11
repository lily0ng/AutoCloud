package main

import (
	"fmt"
	"log"
	"time"
)

type CostOptimizer struct {
	recommendations []Recommendation
}

type Recommendation struct {
	ResourceID   string
	Type         string
	CurrentCost  float64
	OptimizedCost float64
	Savings      float64
	Action       string
}

func NewCostOptimizer() *CostOptimizer {
	return &CostOptimizer{
		recommendations: make([]Recommendation, 0),
	}
}

func (co *CostOptimizer) AnalyzeResources() {
	log.Println("Analyzing cloud resources for cost optimization...")
	
	// Analyze idle instances
	co.findIdleInstances()
	
	// Analyze oversized instances
	co.findOversizedInstances()
	
	// Analyze unused storage
	co.findUnusedStorage()
	
	// Analyze reserved instance opportunities
	co.findReservedInstanceOpportunities()
}

func (co *CostOptimizer) findIdleInstances() {
	// Mock data
	co.recommendations = append(co.recommendations, Recommendation{
		ResourceID:    "i-1234567890",
		Type:          "EC2 Instance",
		CurrentCost:   100.0,
		OptimizedCost: 0.0,
		Savings:       100.0,
		Action:        "Terminate idle instance",
	})
}

func (co *CostOptimizer) findOversizedInstances() {
	co.recommendations = append(co.recommendations, Recommendation{
		ResourceID:    "i-0987654321",
		Type:          "EC2 Instance",
		CurrentCost:   200.0,
		OptimizedCost: 100.0,
		Savings:       100.0,
		Action:        "Downsize from t3.large to t3.medium",
	})
}

func (co *CostOptimizer) findUnusedStorage() {
	co.recommendations = append(co.recommendations, Recommendation{
		ResourceID:    "vol-1234567890",
		Type:          "EBS Volume",
		CurrentCost:   50.0,
		OptimizedCost: 0.0,
		Savings:       50.0,
		Action:        "Delete unattached volume",
	})
}

func (co *CostOptimizer) findReservedInstanceOpportunities() {
	co.recommendations = append(co.recommendations, Recommendation{
		ResourceID:    "i-reserved-candidate",
		Type:          "EC2 Instance",
		CurrentCost:   300.0,
		OptimizedCost: 180.0,
		Savings:       120.0,
		Action:        "Purchase 1-year reserved instance",
	})
}

func (co *CostOptimizer) GenerateReport() {
	fmt.Println("\n💰 Cost Optimization Report")
	fmt.Println("============================")
	
	totalSavings := 0.0
	for _, rec := range co.recommendations {
		fmt.Printf("\n📊 %s (%s)\n", rec.Type, rec.ResourceID)
		fmt.Printf("   Current Cost: $%.2f/month\n", rec.CurrentCost)
		fmt.Printf("   Optimized Cost: $%.2f/month\n", rec.OptimizedCost)
		fmt.Printf("   Potential Savings: $%.2f/month\n", rec.Savings)
		fmt.Printf("   Action: %s\n", rec.Action)
		totalSavings += rec.Savings
	}
	
	fmt.Printf("\n💵 Total Potential Savings: $%.2f/month\n", totalSavings)
	fmt.Printf("   Annual Savings: $%.2f\n", totalSavings*12)
}

func main() {
	optimizer := NewCostOptimizer()
	optimizer.AnalyzeResources()
	optimizer.GenerateReport()
}
