package main

import (
	"encoding/json"
	"fmt"
	"log"
	"time"
)

type LambdaFunction struct {
	Name        string
	Runtime     string
	Handler     string
	Memory      int
	Timeout     int
	Environment map[string]string
	Layers      []string
}

type Invocation struct {
	RequestID    string
	FunctionName string
	Payload      interface{}
	StartTime    time.Time
	Duration     time.Duration
	Status       string
	Result       interface{}
}

type LambdaOrchestrator struct {
	functions   map[string]*LambdaFunction
	invocations []Invocation
}

func NewLambdaOrchestrator() *LambdaOrchestrator {
	return &LambdaOrchestrator{
		functions:   make(map[string]*LambdaFunction),
		invocations: make([]Invocation, 0),
	}
}

func (lo *LambdaOrchestrator) DeployFunction(fn *LambdaFunction) error {
	lo.functions[fn.Name] = fn
	log.Printf("⚡ Lambda function deployed: %s", fn.Name)
	log.Printf("   Runtime: %s", fn.Runtime)
	log.Printf("   Memory: %dMB, Timeout: %ds", fn.Memory, fn.Timeout)
	return nil
}

func (lo *LambdaOrchestrator) InvokeFunction(name string, payload interface{}) (*Invocation, error) {
	fn, exists := lo.functions[name]
	if !exists {
		return nil, fmt.Errorf("function not found: %s", name)
	}
	
	start := time.Now()
	requestID := fmt.Sprintf("req-%d", len(lo.invocations)+1)
	
	log.Printf("🚀 Invoking function: %s", name)
	
	// Simulate execution
	time.Sleep(100 * time.Millisecond)
	
	invocation := Invocation{
		RequestID:    requestID,
		FunctionName: name,
		Payload:      payload,
		StartTime:    start,
		Duration:     time.Since(start),
		Status:       "success",
		Result:       map[string]string{"statusCode": "200", "body": "Success"},
	}
	
	lo.invocations = append(lo.invocations, invocation)
	
	log.Printf("✅ Function executed in %v", invocation.Duration)
	return &invocation, nil
}

func (lo *LambdaOrchestrator) UpdateFunctionCode(name, codeLocation string) error {
	fn, exists := lo.functions[name]
	if !exists {
		return fmt.Errorf("function not found: %s", name)
	}
	
	log.Printf("📦 Updating function code: %s", name)
	log.Printf("   Code location: %s", codeLocation)
	return nil
}

func (lo *LambdaOrchestrator) SetConcurrency(name string, concurrent int) error {
	if _, exists := lo.functions[name]; !exists {
		return fmt.Errorf("function not found: %s", name)
	}
	
	log.Printf("⚙️  Setting concurrency for %s: %d", name, concurrent)
	return nil
}

func (lo *LambdaOrchestrator) GetMetrics(functionName string) {
	fmt.Printf("\n📊 Metrics for %s:\n", functionName)
	
	count := 0
	var totalDuration time.Duration
	errors := 0
	
	for _, inv := range lo.invocations {
		if inv.FunctionName == functionName {
			count++
			totalDuration += inv.Duration
			if inv.Status == "error" {
				errors++
			}
		}
	}
	
	if count > 0 {
		fmt.Printf("  Invocations: %d\n", count)
		fmt.Printf("  Avg Duration: %v\n", totalDuration/time.Duration(count))
		fmt.Printf("  Error Rate: %.2f%%\n", float64(errors)/float64(count)*100)
	}
}

func main() {
	orchestrator := NewLambdaOrchestrator()
	
	// Deploy function
	fn := &LambdaFunction{
		Name:    "process-orders",
		Runtime: "nodejs18.x",
		Handler: "index.handler",
		Memory:  512,
		Timeout: 30,
		Environment: map[string]string{
			"DB_HOST": "db.example.com",
			"STAGE":   "production",
		},
		Layers: []string{"arn:aws:lambda:layer:nodejs-utils"},
	}
	orchestrator.DeployFunction(fn)
	
	// Invoke function
	payload := map[string]interface{}{
		"orderId": "12345",
		"items":   []string{"item1", "item2"},
	}
	orchestrator.InvokeFunction("process-orders", payload)
	
	// Set concurrency
	orchestrator.SetConcurrency("process-orders", 100)
	
	// Get metrics
	orchestrator.GetMetrics("process-orders")
	
	fmt.Println("\n✅ Lambda orchestration complete")
}
