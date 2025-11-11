package rest

import (
	"encoding/json"
	"net/http"
)

type Response struct {
	Success bool        `json:"success"`
	Data    interface{} `json:"data,omitempty"`
	Error   string      `json:"error,omitempty"`
}

type HealthHandler struct{}

func (h *HealthHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	response := Response{
		Success: true,
		Data: map[string]interface{}{
			"status": "healthy",
			"uptime": "24h",
		},
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

type StatusHandler struct{}

func (h *StatusHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	response := Response{
		Success: true,
		Data: map[string]interface{}{
			"version":     "1.0.0",
			"environment": "production",
			"services": map[string]string{
				"database": "connected",
				"cache":    "connected",
				"queue":    "connected",
			},
		},
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

type MetricsHandler struct{}

func (h *MetricsHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain")
	w.Write([]byte("# HELP http_requests_total Total HTTP requests\n"))
	w.Write([]byte("# TYPE http_requests_total counter\n"))
	w.Write([]byte("http_requests_total 1000\n"))
}
