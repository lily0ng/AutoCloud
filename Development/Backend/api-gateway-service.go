package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"
)

type Route struct {
	Path        string
	Method      string
	Service     string
	Endpoint    string
	RateLimit   int
	Timeout     time.Duration
	AuthRequired bool
}

type APIGateway struct {
	routes       []Route
	rateLimiter  map[string]int
	circuitBreaker map[string]bool
}

func NewAPIGateway() *APIGateway {
	return &APIGateway{
		routes:       make([]Route, 0),
		rateLimiter:  make(map[string]int),
		circuitBreaker: make(map[string]bool),
	}
}

func (ag *APIGateway) RegisterRoute(route Route) {
	ag.routes = append(ag.routes, route)
	log.Printf("🌐 Route registered: %s %s -> %s%s", route.Method, route.Path, route.Service, route.Endpoint)
}

func (ag *APIGateway) HandleRequest(method, path string, headers map[string]string) (int, interface{}) {
	// Find matching route
	var matchedRoute *Route
	for _, route := range ag.routes {
		if route.Method == method && route.Path == path {
			matchedRoute = &route
			break
		}
	}
	
	if matchedRoute == nil {
		return http.StatusNotFound, map[string]string{"error": "Route not found"}
	}
	
	// Check authentication
	if matchedRoute.AuthRequired {
		if !ag.authenticate(headers) {
			return http.StatusUnauthorized, map[string]string{"error": "Unauthorized"}
		}
	}
	
	// Check rate limit
	if !ag.checkRateLimit(matchedRoute.Service) {
		return http.StatusTooManyRequests, map[string]string{"error": "Rate limit exceeded"}
	}
	
	// Check circuit breaker
	if ag.circuitBreaker[matchedRoute.Service] {
		return http.StatusServiceUnavailable, map[string]string{"error": "Service unavailable"}
	}
	
	// Forward request
	log.Printf("→ Forwarding: %s %s to %s", method, path, matchedRoute.Service)
	response := ag.forwardRequest(matchedRoute)
	
	return http.StatusOK, response
}

func (ag *APIGateway) authenticate(headers map[string]string) bool {
	token, exists := headers["Authorization"]
	if !exists || token == "" {
		return false
	}
	// Mock authentication
	return token == "Bearer valid-token"
}

func (ag *APIGateway) checkRateLimit(service string) bool {
	count := ag.rateLimiter[service]
	if count >= 100 {
		log.Printf("⚠️  Rate limit exceeded for %s", service)
		return false
	}
	ag.rateLimiter[service] = count + 1
	return true
}

func (ag *APIGateway) forwardRequest(route *Route) interface{} {
	// Simulate request forwarding
	time.Sleep(50 * time.Millisecond)
	return map[string]interface{}{
		"service": route.Service,
		"data":    "Response from " + route.Service,
		"timestamp": time.Now().Unix(),
	}
}

func (ag *APIGateway) OpenCircuit(service string) {
	ag.circuitBreaker[service] = true
	log.Printf("🔴 Circuit opened for %s", service)
}

func (ag *APIGateway) CloseCircuit(service string) {
	ag.circuitBreaker[service] = false
	log.Printf("🟢 Circuit closed for %s", service)
}

func (ag *APIGateway) GetMetrics() map[string]interface{} {
	totalRequests := 0
	for _, count := range ag.rateLimiter {
		totalRequests += count
	}
	
	return map[string]interface{}{
		"total_requests": totalRequests,
		"total_routes":   len(ag.routes),
		"services":       len(ag.rateLimiter),
		"circuit_breakers": ag.circuitBreaker,
	}
}

func main() {
	gateway := NewAPIGateway()
	
	// Register routes
	gateway.RegisterRoute(Route{
		Path:        "/api/users",
		Method:      "GET",
		Service:     "user-service",
		Endpoint:    "/users",
		RateLimit:   100,
		Timeout:     5 * time.Second,
		AuthRequired: true,
	})
	
	gateway.RegisterRoute(Route{
		Path:        "/api/orders",
		Method:      "POST",
		Service:     "order-service",
		Endpoint:    "/orders",
		RateLimit:   50,
		Timeout:     10 * time.Second,
		AuthRequired: true,
	})
	
	gateway.RegisterRoute(Route{
		Path:        "/api/health",
		Method:      "GET",
		Service:     "health-service",
		Endpoint:    "/health",
		RateLimit:   1000,
		Timeout:     1 * time.Second,
		AuthRequired: false,
	})
	
	// Handle requests
	headers := map[string]string{"Authorization": "Bearer valid-token"}
	
	status, response := gateway.HandleRequest("GET", "/api/users", headers)
	fmt.Printf("\n📥 Request: GET /api/users\n")
	fmt.Printf("   Status: %d\n", status)
	responseJSON, _ := json.MarshalIndent(response, "   ", "  ")
	fmt.Printf("   Response: %s\n", string(responseJSON))
	
	// Get metrics
	fmt.Println("\n📊 Gateway Metrics:")
	metrics := gateway.GetMetrics()
	metricsJSON, _ := json.MarshalIndent(metrics, "   ", "  ")
	fmt.Printf("   %s\n", string(metricsJSON))
	
	fmt.Println("\n✅ API Gateway operational")
}
