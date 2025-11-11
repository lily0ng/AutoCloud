package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

type APIServer struct {
	router *mux.Router
	port   string
}

type Response struct {
	Success bool        `json:"success"`
	Data    interface{} `json:"data,omitempty"`
	Error   string      `json:"error,omitempty"`
	Meta    Meta        `json:"meta"`
}

type Meta struct {
	Timestamp time.Time `json:"timestamp"`
	Version   string    `json:"version"`
}

func NewAPIServer(port string) *APIServer {
	return &APIServer{
		router: mux.NewRouter(),
		port:   port,
	}
}

func (s *APIServer) setupRoutes() {
	s.router.HandleFunc("/api/v1/health", s.healthHandler).Methods("GET")
	s.router.HandleFunc("/api/v1/users", s.listUsersHandler).Methods("GET")
	s.router.HandleFunc("/api/v1/users", s.createUserHandler).Methods("POST")
	s.router.HandleFunc("/api/v1/users/{id}", s.getUserHandler).Methods("GET")
	s.router.HandleFunc("/api/v1/users/{id}", s.updateUserHandler).Methods("PUT")
	s.router.HandleFunc("/api/v1/users/{id}", s.deleteUserHandler).Methods("DELETE")
	
	s.router.Use(loggingMiddleware)
	s.router.Use(corsMiddleware)
}

func (s *APIServer) healthHandler(w http.ResponseWriter, r *http.Request) {
	respondJSON(w, http.StatusOK, Response{
		Success: true,
		Data: map[string]interface{}{
			"status": "healthy",
			"uptime": "24h",
		},
		Meta: Meta{
			Timestamp: time.Now(),
			Version:   "1.0.0",
		},
	})
}

func (s *APIServer) listUsersHandler(w http.ResponseWriter, r *http.Request) {
	users := []map[string]interface{}{
		{"id": 1, "name": "John Doe", "email": "john@example.com"},
		{"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
	}
	
	respondJSON(w, http.StatusOK, Response{
		Success: true,
		Data:    users,
		Meta:    Meta{Timestamp: time.Now(), Version: "1.0.0"},
	})
}

func (s *APIServer) createUserHandler(w http.ResponseWriter, r *http.Request) {
	var user map[string]interface{}
	if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
		respondJSON(w, http.StatusBadRequest, Response{
			Success: false,
			Error:   "Invalid request body",
			Meta:    Meta{Timestamp: time.Now(), Version: "1.0.0"},
		})
		return
	}
	
	user["id"] = 3
	respondJSON(w, http.StatusCreated, Response{
		Success: true,
		Data:    user,
		Meta:    Meta{Timestamp: time.Now(), Version: "1.0.0"},
	})
}

func (s *APIServer) getUserHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	userID := vars["id"]
	
	user := map[string]interface{}{
		"id":    userID,
		"name":  "John Doe",
		"email": "john@example.com",
	}
	
	respondJSON(w, http.StatusOK, Response{
		Success: true,
		Data:    user,
		Meta:    Meta{Timestamp: time.Now(), Version: "1.0.0"},
	})
}

func (s *APIServer) updateUserHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	userID := vars["id"]
	
	var updates map[string]interface{}
	if err := json.NewDecoder(r.Body).Decode(&updates); err != nil {
		respondJSON(w, http.StatusBadRequest, Response{
			Success: false,
			Error:   "Invalid request body",
			Meta:    Meta{Timestamp: time.Now(), Version: "1.0.0"},
		})
		return
	}
	
	updates["id"] = userID
	respondJSON(w, http.StatusOK, Response{
		Success: true,
		Data:    updates,
		Meta:    Meta{Timestamp: time.Now(), Version: "1.0.0"},
	})
}

func (s *APIServer) deleteUserHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	userID := vars["id"]
	
	respondJSON(w, http.StatusOK, Response{
		Success: true,
		Data:    map[string]string{"deleted": userID},
		Meta:    Meta{Timestamp: time.Now(), Version: "1.0.0"},
	})
}

func respondJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}

func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		log.Printf("%s %s", r.Method, r.URL.Path)
		next.ServeHTTP(w, r)
		log.Printf("Completed in %v", time.Since(start))
	})
}

func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
		
		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}
		
		next.ServeHTTP(w, r)
	})
}

func (s *APIServer) Start() error {
	s.setupRoutes()
	log.Printf("API Server starting on port %s", s.port)
	return http.ListenAndServe(":"+s.port, s.router)
}

func main() {
	server := NewAPIServer("8080")
	log.Fatal(server.Start())
}
