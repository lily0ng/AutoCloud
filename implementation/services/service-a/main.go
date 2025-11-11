package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/mux"
)

type ServiceA struct {
	Name    string
	Version string
	Port    string
}

type HealthResponse struct {
	Status    string    `json:"status"`
	Service   string    `json:"service"`
	Timestamp time.Time `json:"timestamp"`
}

type DataResponse struct {
	Message string      `json:"message"`
	Data    interface{} `json:"data"`
	Service string      `json:"service"`
}

func (s *ServiceA) healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	response := HealthResponse{
		Status:    "healthy",
		Service:   s.Name,
		Timestamp: time.Now(),
	}
	json.NewEncoder(w).Encode(response)
}

func (s *ServiceA) processHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	
	var requestData map[string]interface{}
	if err := json.NewDecoder(r.Body).Decode(&requestData); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	response := DataResponse{
		Message: "Data processed successfully",
		Data:    requestData,
		Service: s.Name,
	}
	json.NewEncoder(w).Encode(response)
}

func (s *ServiceA) metricsHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain")
	fmt.Fprintf(w, "# HELP service_a_requests_total Total requests\n")
	fmt.Fprintf(w, "# TYPE service_a_requests_total counter\n")
	fmt.Fprintf(w, "service_a_requests_total 1000\n")
}

func main() {
	service := &ServiceA{
		Name:    "Service-A",
		Version: "1.0.0",
		Port:    getEnv("PORT", "8080"),
	}

	router := mux.NewRouter()
	router.HandleFunc("/health", service.healthHandler).Methods("GET")
	router.HandleFunc("/api/v1/process", service.processHandler).Methods("POST")
	router.HandleFunc("/metrics", service.metricsHandler).Methods("GET")

	log.Printf("Starting %s on port %s\n", service.Name, service.Port)
	log.Fatal(http.ListenAndServe(":"+service.Port, router))
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
