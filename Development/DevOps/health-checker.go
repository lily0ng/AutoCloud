package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type HealthStatus struct {
	Status    string    `json:"status"`
	Timestamp time.Time `json:"timestamp"`
	Uptime    float64   `json:"uptime"`
}

var startTime = time.Now()

func healthHandler(w http.ResponseWriter, r *http.Request) {
	uptime := time.Since(startTime).Seconds()
	
	status := HealthStatus{
		Status:    "healthy",
		Timestamp: time.Now(),
		Uptime:    uptime,
	}
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(status)
}

func main() {
	http.HandleFunc("/health", healthHandler)
	log.Println("Health checker running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
