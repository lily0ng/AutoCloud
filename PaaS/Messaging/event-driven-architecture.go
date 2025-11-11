package main

import (
	"encoding/json"
	"fmt"
	"log"
	"time"
)

type Event struct {
	ID        string
	Type      string
	Source    string
	Data      interface{}
	Timestamp time.Time
}

type EventHandler func(Event) error

type EventBus struct {
	handlers map[string][]EventHandler
	events   []Event
}

func NewEventBus() *EventBus {
	return &EventBus{
		handlers: make(map[string][]EventHandler),
		events:   make([]Event, 0),
	}
}

func (eb *EventBus) Subscribe(eventType string, handler EventHandler) {
	eb.handlers[eventType] = append(eb.handlers[eventType], handler)
	log.Printf("📡 Subscribed to event: %s", eventType)
}

func (eb *EventBus) Publish(event Event) error {
	event.ID = fmt.Sprintf("evt-%d", time.Now().UnixNano())
	event.Timestamp = time.Now()
	
	eb.events = append(eb.events, event)
	
	log.Printf("📤 Publishing event: %s from %s", event.Type, event.Source)
	
	handlers, exists := eb.handlers[event.Type]
	if !exists {
		log.Printf("⚠️  No handlers for event type: %s", event.Type)
		return nil
	}
	
	for _, handler := range handlers {
		if err := handler(event); err != nil {
			log.Printf("❌ Handler error: %v", err)
			return err
		}
	}
	
	return nil
}

func (eb *EventBus) GetEventHistory(eventType string, limit int) []Event {
	history := make([]Event, 0)
	count := 0
	
	for i := len(eb.events) - 1; i >= 0 && count < limit; i-- {
		if eventType == "" || eb.events[i].Type == eventType {
			history = append(history, eb.events[i])
			count++
		}
	}
	
	return history
}

// Example event handlers
func handleUserCreated(event Event) error {
	log.Printf("👤 User created handler: %v", event.Data)
	// Send welcome email
	// Create user profile
	return nil
}

func handleOrderPlaced(event Event) error {
	log.Printf("🛒 Order placed handler: %v", event.Data)
	// Process payment
	// Update inventory
	// Send confirmation
	return nil
}

func handlePaymentProcessed(event Event) error {
	log.Printf("💳 Payment processed handler: %v", event.Data)
	// Update order status
	// Send receipt
	return nil
}

func main() {
	eventBus := NewEventBus()
	
	// Subscribe to events
	eventBus.Subscribe("user.created", handleUserCreated)
	eventBus.Subscribe("order.placed", handleOrderPlaced)
	eventBus.Subscribe("payment.processed", handlePaymentProcessed)
	
	// Publish events
	eventBus.Publish(Event{
		Type:   "user.created",
		Source: "user-service",
		Data: map[string]interface{}{
			"userId": "user-123",
			"email":  "user@example.com",
		},
	})
	
	eventBus.Publish(Event{
		Type:   "order.placed",
		Source: "order-service",
		Data: map[string]interface{}{
			"orderId": "order-456",
			"userId":  "user-123",
			"total":   99.99,
		},
	})
	
	eventBus.Publish(Event{
		Type:   "payment.processed",
		Source: "payment-service",
		Data: map[string]interface{}{
			"orderId":     "order-456",
			"amount":      99.99,
			"status":      "success",
			"transaction": "txn-789",
		},
	})
	
	// Get event history
	fmt.Println("\n📜 Recent Events:")
	history := eventBus.GetEventHistory("", 5)
	for _, evt := range history {
		data, _ := json.MarshalIndent(evt.Data, "  ", "  ")
		fmt.Printf("  %s - %s (%s)\n  %s\n", 
			evt.Timestamp.Format("15:04:05"), evt.Type, evt.Source, string(data))
	}
	
	fmt.Println("\n✅ Event-driven architecture operational")
}
