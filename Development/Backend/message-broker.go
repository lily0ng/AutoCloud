package main

import (
	"fmt"
	"log"
	"sync"
	"time"
)

type Message struct {
	ID        string
	Topic     string
	Payload   interface{}
	Timestamp time.Time
	Headers   map[string]string
}

type Subscriber struct {
	ID      string
	Topic   string
	Handler func(Message)
}

type MessageBroker struct {
	topics      map[string][]Message
	subscribers map[string][]*Subscriber
	mu          sync.RWMutex
}

func NewMessageBroker() *MessageBroker {
	return &MessageBroker{
		topics:      make(map[string][]Message),
		subscribers: make(map[string][]*Subscriber),
	}
}

func (mb *MessageBroker) CreateTopic(topic string) {
	mb.mu.Lock()
	defer mb.mu.Unlock()
	
	if _, exists := mb.topics[topic]; !exists {
		mb.topics[topic] = make([]Message, 0)
		log.Printf("📋 Topic created: %s", topic)
	}
}

func (mb *MessageBroker) Publish(topic string, payload interface{}) error {
	mb.mu.Lock()
	
	message := Message{
		ID:        fmt.Sprintf("msg-%d", time.Now().UnixNano()),
		Topic:     topic,
		Payload:   payload,
		Timestamp: time.Now(),
		Headers:   make(map[string]string),
	}
	
	mb.topics[topic] = append(mb.topics[topic], message)
	subscribers := mb.subscribers[topic]
	
	mb.mu.Unlock()
	
	log.Printf("📤 Published to %s: %s", topic, message.ID)
	
	// Notify subscribers
	for _, sub := range subscribers {
		go sub.Handler(message)
	}
	
	return nil
}

func (mb *MessageBroker) Subscribe(topic string, handler func(Message)) string {
	mb.mu.Lock()
	defer mb.mu.Unlock()
	
	subscriberID := fmt.Sprintf("sub-%d", time.Now().UnixNano())
	
	subscriber := &Subscriber{
		ID:      subscriberID,
		Topic:   topic,
		Handler: handler,
	}
	
	mb.subscribers[topic] = append(mb.subscribers[topic], subscriber)
	log.Printf("📥 Subscribed to %s: %s", topic, subscriberID)
	
	return subscriberID
}

func (mb *MessageBroker) Unsubscribe(topic, subscriberID string) {
	mb.mu.Lock()
	defer mb.mu.Unlock()
	
	subscribers := mb.subscribers[topic]
	newSubscribers := make([]*Subscriber, 0)
	
	for _, sub := range subscribers {
		if sub.ID != subscriberID {
			newSubscribers = append(newSubscribers, sub)
		}
	}
	
	mb.subscribers[topic] = newSubscribers
	log.Printf("🔌 Unsubscribed from %s: %s", topic, subscriberID)
}

func (mb *MessageBroker) GetMessages(topic string, limit int) []Message {
	mb.mu.RLock()
	defer mb.mu.RUnlock()
	
	messages := mb.topics[topic]
	if len(messages) == 0 {
		return []Message{}
	}
	
	start := len(messages) - limit
	if start < 0 {
		start = 0
	}
	
	return messages[start:]
}

func (mb *MessageBroker) GetTopicStats() map[string]interface{} {
	mb.mu.RLock()
	defer mb.mu.RUnlock()
	
	stats := make(map[string]interface{})
	
	for topic, messages := range mb.topics {
		stats[topic] = map[string]interface{}{
			"messages":    len(messages),
			"subscribers": len(mb.subscribers[topic]),
		}
	}
	
	return stats
}

func main() {
	broker := NewMessageBroker()
	
	// Create topics
	broker.CreateTopic("orders")
	broker.CreateTopic("notifications")
	broker.CreateTopic("analytics")
	
	// Subscribe to topics
	broker.Subscribe("orders", func(msg Message) {
		log.Printf("📦 Order handler received: %v", msg.Payload)
	})
	
	broker.Subscribe("notifications", func(msg Message) {
		log.Printf("🔔 Notification handler received: %v", msg.Payload)
	})
	
	broker.Subscribe("analytics", func(msg Message) {
		log.Printf("📊 Analytics handler received: %v", msg.Payload)
	})
	
	// Publish messages
	broker.Publish("orders", map[string]interface{}{
		"orderId": "ORD-123",
		"amount":  99.99,
		"status":  "pending",
	})
	
	broker.Publish("notifications", map[string]interface{}{
		"type":    "email",
		"to":      "user@example.com",
		"subject": "Order Confirmation",
	})
	
	broker.Publish("analytics", map[string]interface{}{
		"event":  "page_view",
		"page":   "/products",
		"userId": "user-456",
	})
	
	time.Sleep(100 * time.Millisecond)
	
	// Get topic stats
	fmt.Println("\n📊 Topic Statistics:")
	stats := broker.GetTopicStats()
	for topic, data := range stats {
		fmt.Printf("   %s: %v\n", topic, data)
	}
	
	fmt.Println("\n✅ Message broker operational")
}
