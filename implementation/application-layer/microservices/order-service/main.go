package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

type Order struct {
	ID         string    `json:"id"`
	CustomerID string    `json:"customer_id"`
	Items      []Item    `json:"items"`
	Total      float64   `json:"total"`
	Status     string    `json:"status"`
	CreatedAt  time.Time `json:"created_at"`
}

type Item struct {
	ProductID string  `json:"product_id"`
	Quantity  int     `json:"quantity"`
	Price     float64 `json:"price"`
}

type OrderService struct {
	orders map[string]*Order
}

func NewOrderService() *OrderService {
	return &OrderService{
		orders: make(map[string]*Order),
	}
}

func (s *OrderService) CreateOrder(w http.ResponseWriter, r *http.Request) {
	var order Order
	if err := json.NewDecoder(r.Body).Decode(&order); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	order.ID = generateOrderID()
	order.Status = "pending"
	order.CreatedAt = time.Now()
	
	// Calculate total
	var total float64
	for _, item := range order.Items {
		total += item.Price * float64(item.Quantity)
	}
	order.Total = total

	s.orders[order.ID] = &order

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(order)
}

func (s *OrderService) GetOrder(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	orderID := vars["id"]

	order, exists := s.orders[orderID]
	if !exists {
		http.Error(w, "Order not found", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(order)
}

func (s *OrderService) ListOrders(w http.ResponseWriter, r *http.Request) {
	orders := make([]*Order, 0, len(s.orders))
	for _, order := range s.orders {
		orders = append(orders, order)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(orders)
}

func (s *OrderService) UpdateOrderStatus(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	orderID := vars["id"]

	var update struct {
		Status string `json:"status"`
	}
	if err := json.NewDecoder(r.Body).Decode(&update); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	order, exists := s.orders[orderID]
	if !exists {
		http.Error(w, "Order not found", http.StatusNotFound)
		return
	}

	order.Status = update.Status

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(order)
}

func generateOrderID() string {
	return "ORD-" + time.Now().Format("20060102150405")
}

func main() {
	service := NewOrderService()
	router := mux.NewRouter()

	router.HandleFunc("/api/v1/orders", service.CreateOrder).Methods("POST")
	router.HandleFunc("/api/v1/orders", service.ListOrders).Methods("GET")
	router.HandleFunc("/api/v1/orders/{id}", service.GetOrder).Methods("GET")
	router.HandleFunc("/api/v1/orders/{id}/status", service.UpdateOrderStatus).Methods("PUT")

	log.Println("Order Service started on :8083")
	log.Fatal(http.ListenAndServe(":8083", router))
}
