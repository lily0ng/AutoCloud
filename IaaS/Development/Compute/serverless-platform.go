package main

import (
	"context"
	"fmt"
	"log"
	"time"
)

type Function struct {
	Name    string
	Runtime string
	Handler string
	Memory  int
	Timeout int
	Code    string
}

type Invocation struct {
	FunctionName string
	RequestID    string
	StartTime    time.Time
	Duration     time.Duration
	Status       string
}

type ServerlessPlatform struct {
	functions   map[string]*Function
	invocations []Invocation
}

func NewServerlessPlatform() *ServerlessPlatform {
	return &ServerlessPlatform{
		functions:   make(map[string]*Function),
		invocations: make([]Invocation, 0),
	}
}

func (sp *ServerlessPlatform) DeployFunction(fn *Function) error {
	sp.functions[fn.Name] = fn
	log.Printf("📦 Function deployed: %s (%s)", fn.Name, fn.Runtime)
	return nil
}

func (sp *ServerlessPlatform) InvokeFunction(ctx context.Context, name string, payload interface{}) (interface{}, error) {
	fn, exists := sp.functions[name]
	if !exists {
		return nil, fmt.Errorf("function not found: %s", name)
	}
	
	start := time.Now()
	requestID := fmt.Sprintf("req-%d", len(sp.invocations)+1)
	
	log.Printf("⚡ Invoking function: %s", name)
	
	// Simulate execution
	time.Sleep(100 * time.Millisecond)
	
	invocation := Invocation{
		FunctionName: name,
		RequestID:    requestID,
		StartTime:    start,
		Duration:     time.Since(start),
		Status:       "success",
	}
	
	sp.invocations = append(sp.invocations, invocation)
	
	log.Printf("✅ Function executed in %v", invocation.Duration)
	return map[string]string{"result": "success"}, nil
}

func (sp *ServerlessPlatform) GetMetrics(functionName string) {
	fmt.Printf("\n📊 Metrics for %s:\n", functionName)
	
	count := 0
	var totalDuration time.Duration
	
	for _, inv := range sp.invocations {
		if inv.FunctionName == functionName {
			count++
			totalDuration += inv.Duration
		}
	}
	
	if count > 0 {
		fmt.Printf("  Invocations: %d\n", count)
		fmt.Printf("  Avg Duration: %v\n", totalDuration/time.Duration(count))
	}
}

func main() {
	platform := NewServerlessPlatform()
	
	platform.DeployFunction(&Function{
		Name:    "hello-world",
		Runtime: "nodejs18",
		Handler: "index.handler",
		Memory:  256,
		Timeout: 30,
	})
	
	ctx := context.Background()
	platform.InvokeFunction(ctx, "hello-world", map[string]string{"name": "user"})
	platform.GetMetrics("hello-world")
}
