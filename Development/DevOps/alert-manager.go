package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type Alert struct {
	Name     string    `json:"name"`
	Severity string    `json:"severity"`
	Message  string    `json:"message"`
	Time     time.Time `json:"time"`
}

var alerts []Alert

func createAlert(w http.ResponseWriter, r *http.Request) {
	var alert Alert
	json.NewDecoder(r.Body).Decode(&alert)
	alert.Time = time.Now()
	alerts = append(alerts, alert)
	
	log.Printf("Alert: %s - %s", alert.Severity, alert.Message)
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(alert)
}

func getAlerts(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(alerts)
}

func main() {
	http.HandleFunc("/alerts", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == "POST" {
			createAlert(w, r)
		} else {
			getAlerts(w, r)
		}
	})
	
	log.Println("Alert manager running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
