package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/mux"
)

type ServiceC struct {
	Name    string
	Version string
	Port    string
}

type ReportRequest struct {
	StartDate time.Time `json:"start_date"`
	EndDate   time.Time `json:"end_date"`
	Type      string    `json:"type"`
}

type ReportResponse struct {
	ReportID  string                 `json:"report_id"`
	Status    string                 `json:"status"`
	Data      map[string]interface{} `json:"data"`
	Generated time.Time              `json:"generated"`
}

func (s *ServiceC) healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"status":    "healthy",
		"service":   s.Name,
		"timestamp": time.Now(),
	})
}

func (s *ServiceC) reportHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	var req ReportRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	response := ReportResponse{
		ReportID: "RPT-" + time.Now().Format("20060102150405"),
		Status:   "generated",
		Data: map[string]interface{}{
			"total_records": 1500,
			"summary":       "Report generated successfully",
		},
		Generated: time.Now(),
	}

	json.NewEncoder(w).Encode(response)
}

func (s *ServiceC) exportHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"export_id": "EXP-" + time.Now().Format("20060102150405"),
		"format":    "csv",
		"status":    "ready",
		"service":   s.Name,
	})
}

func main() {
	service := &ServiceC{
		Name:    "Service-C",
		Version: "1.0.0",
		Port:    getEnv("PORT", "8082"),
	}

	router := mux.NewRouter()
	router.HandleFunc("/health", service.healthHandler).Methods("GET")
	router.HandleFunc("/api/v1/report", service.reportHandler).Methods("POST")
	router.HandleFunc("/api/v1/export", service.exportHandler).Methods("GET")

	log.Printf("Starting %s on port %s\n", service.Name, service.Port)
	log.Fatal(http.ListenAndServe(":"+service.Port, router))
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
