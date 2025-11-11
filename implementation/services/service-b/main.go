package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/mux"
)

type ServiceB struct {
	Name    string
	Version string
	Port    string
}

type TransactionRequest struct {
	ID     string                 `json:"id"`
	Type   string                 `json:"type"`
	Amount float64                `json:"amount"`
	Data   map[string]interface{} `json:"data"`
}

type TransactionResponse struct {
	TransactionID string    `json:"transaction_id"`
	Status        string    `json:"status"`
	Timestamp     time.Time `json:"timestamp"`
	Service       string    `json:"service"`
}

func (s *ServiceB) healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"status":    "healthy",
		"service":   s.Name,
		"timestamp": time.Now(),
	})
}

func (s *ServiceB) transactionHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	var req TransactionRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	response := TransactionResponse{
		TransactionID: req.ID,
		Status:        "processed",
		Timestamp:     time.Now(),
		Service:       s.Name,
	}

	json.NewEncoder(w).Encode(response)
}

func (s *ServiceB) analyticsHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"total_transactions": 5000,
		"success_rate":       99.5,
		"avg_response_time":  "45ms",
		"service":            s.Name,
	})
}

func main() {
	service := &ServiceB{
		Name:    "Service-B",
		Version: "1.0.0",
		Port:    getEnv("PORT", "8081"),
	}

	router := mux.NewRouter()
	router.HandleFunc("/health", service.healthHandler).Methods("GET")
	router.HandleFunc("/api/v1/transaction", service.transactionHandler).Methods("POST")
	router.HandleFunc("/api/v1/analytics", service.analyticsHandler).Methods("GET")

	log.Printf("Starting %s on port %s\n", service.Name, service.Port)
	log.Fatal(http.ListenAndServe(":"+service.Port, router))
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
