package main

import (
	"context"
	"encoding/json"
	"log"
	"time"

	"github.com/segmentio/kafka-go"
)

type QueueClient struct {
	writer *kafka.Writer
	reader *kafka.Reader
}

type Message struct {
	ID        string                 `json:"id"`
	Type      string                 `json:"type"`
	Payload   map[string]interface{} `json:"payload"`
	Timestamp time.Time              `json:"timestamp"`
}

func NewQueueClient(brokers []string, topic string) *QueueClient {
	writer := &kafka.Writer{
		Addr:         kafka.TCP(brokers...),
		Topic:        topic,
		Balancer:     &kafka.LeastBytes{},
		BatchSize:    100,
		BatchTimeout: 10 * time.Millisecond,
	}

	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers:  brokers,
		Topic:    topic,
		GroupID:  "service-b-consumer",
		MinBytes: 10e3,
		MaxBytes: 10e6,
	})

	return &QueueClient{
		writer: writer,
		reader: reader,
	}
}

func (q *QueueClient) Publish(msg Message) error {
	data, err := json.Marshal(msg)
	if err != nil {
		return err
	}

	return q.writer.WriteMessages(context.Background(),
		kafka.Message{
			Key:   []byte(msg.ID),
			Value: data,
		},
	)
}

func (q *QueueClient) Consume() (*Message, error) {
	m, err := q.reader.ReadMessage(context.Background())
	if err != nil {
		return nil, err
	}

	var msg Message
	if err := json.Unmarshal(m.Value, &msg); err != nil {
		return nil, err
	}

	return &msg, nil
}

func (q *QueueClient) Close() error {
	if err := q.writer.Close(); err != nil {
		log.Printf("Error closing writer: %v", err)
	}
	if err := q.reader.Close(); err != nil {
		log.Printf("Error closing reader: %v", err)
	}
	return nil
}
