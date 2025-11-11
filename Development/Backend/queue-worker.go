package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"time"

	"github.com/hibiken/asynq"
)

const (
	TypeEmailDelivery     = "email:delivery"
	TypeImageResize       = "image:resize"
	TypeDataProcessing    = "data:processing"
	TypeNotification      = "notification:send"
	TypeReportGeneration  = "report:generation"
)

// Task payloads
type EmailDeliveryPayload struct {
	To      string `json:"to"`
	Subject string `json:"subject"`
	Body    string `json:"body"`
}

type ImageResizePayload struct {
	SourceURL string `json:"source_url"`
	Width     int    `json:"width"`
	Height    int    `json:"height"`
}

type DataProcessingPayload struct {
	DataID string `json:"data_id"`
	Type   string `json:"type"`
}

// QueueClient handles task enqueueing
type QueueClient struct {
	client *asynq.Client
}

// NewQueueClient creates a new queue client
func NewQueueClient(redisAddr string) *QueueClient {
	client := asynq.NewClient(asynq.RedisClientOpt{Addr: redisAddr})
	return &QueueClient{client: client}
}

// EnqueueEmailDelivery enqueues an email delivery task
func (qc *QueueClient) EnqueueEmailDelivery(payload EmailDeliveryPayload, opts ...asynq.Option) error {
	data, err := json.Marshal(payload)
	if err != nil {
		return err
	}

	task := asynq.NewTask(TypeEmailDelivery, data, opts...)
	info, err := qc.client.Enqueue(task)
	if err != nil {
		return err
	}

	log.Printf("Enqueued task: id=%s queue=%s", info.ID, info.Queue)
	return nil
}

// EnqueueImageResize enqueues an image resize task
func (qc *QueueClient) EnqueueImageResize(payload ImageResizePayload, opts ...asynq.Option) error {
	data, err := json.Marshal(payload)
	if err != nil {
		return err
	}

	task := asynq.NewTask(TypeImageResize, data, opts...)
	info, err := qc.client.Enqueue(task)
	if err != nil {
		return err
	}

	log.Printf("Enqueued task: id=%s queue=%s", info.ID, info.Queue)
	return nil
}

// EnqueueDataProcessing enqueues a data processing task
func (qc *QueueClient) EnqueueDataProcessing(payload DataProcessingPayload, opts ...asynq.Option) error {
	data, err := json.Marshal(payload)
	if err != nil {
		return err
	}

	task := asynq.NewTask(TypeDataProcessing, data, opts...)
	info, err := qc.client.Enqueue(task)
	if err != nil {
		return err
	}

	log.Printf("Enqueued task: id=%s queue=%s", info.ID, info.Queue)
	return nil
}

// Close closes the queue client
func (qc *QueueClient) Close() error {
	return qc.client.Close()
}

// Task handlers
func HandleEmailDelivery(ctx context.Context, t *asynq.Task) error {
	var payload EmailDeliveryPayload
	if err := json.Unmarshal(t.Payload(), &payload); err != nil {
		return fmt.Errorf("failed to unmarshal payload: %w", err)
	}

	log.Printf("Sending email to %s: %s", payload.To, payload.Subject)
	
	// Simulate email sending
	time.Sleep(2 * time.Second)
	
	log.Printf("Email sent successfully to %s", payload.To)
	return nil
}

func HandleImageResize(ctx context.Context, t *asynq.Task) error {
	var payload ImageResizePayload
	if err := json.Unmarshal(t.Payload(), &payload); err != nil {
		return fmt.Errorf("failed to unmarshal payload: %w", err)
	}

	log.Printf("Resizing image: %s to %dx%d", payload.SourceURL, payload.Width, payload.Height)
	
	// Simulate image processing
	time.Sleep(3 * time.Second)
	
	log.Printf("Image resized successfully: %s", payload.SourceURL)
	return nil
}

func HandleDataProcessing(ctx context.Context, t *asynq.Task) error {
	var payload DataProcessingPayload
	if err := json.Unmarshal(t.Payload(), &payload); err != nil {
		return fmt.Errorf("failed to unmarshal payload: %w", err)
	}

	log.Printf("Processing data: %s (type: %s)", payload.DataID, payload.Type)
	
	// Simulate data processing
	time.Sleep(5 * time.Second)
	
	log.Printf("Data processed successfully: %s", payload.DataID)
	return nil
}

// Worker server
type WorkerServer struct {
	server *asynq.Server
}

// NewWorkerServer creates a new worker server
func NewWorkerServer(redisAddr string, concurrency int) *WorkerServer {
	srv := asynq.NewServer(
		asynq.RedisClientOpt{Addr: redisAddr},
		asynq.Config{
			Concurrency: concurrency,
			Queues: map[string]int{
				"critical": 6,
				"default":  3,
				"low":      1,
			},
			RetryDelayFunc: func(n int, err error, task *asynq.Task) time.Duration {
				return time.Duration(n) * time.Minute
			},
			ErrorHandler: asynq.ErrorHandlerFunc(func(ctx context.Context, task *asynq.Task, err error) {
				log.Printf("Task failed: type=%s error=%v", task.Type(), err)
			}),
		},
	)

	return &WorkerServer{server: srv}
}

// Start starts the worker server
func (ws *WorkerServer) Start() error {
	mux := asynq.NewServeMux()

	// Register task handlers
	mux.HandleFunc(TypeEmailDelivery, HandleEmailDelivery)
	mux.HandleFunc(TypeImageResize, HandleImageResize)
	mux.HandleFunc(TypeDataProcessing, HandleDataProcessing)

	log.Println("Starting worker server...")
	return ws.server.Run(mux)
}

// Stop stops the worker server
func (ws *WorkerServer) Stop() {
	ws.server.Shutdown()
}

func main() {
	redisAddr := "localhost:6379"

	// Start worker server in a goroutine
	worker := NewWorkerServer(redisAddr, 10)
	go func() {
		if err := worker.Start(); err != nil {
			log.Fatal(err)
		}
	}()

	// Example: Enqueue some tasks
	client := NewQueueClient(redisAddr)
	defer client.Close()

	// Enqueue email task
	err := client.EnqueueEmailDelivery(
		EmailDeliveryPayload{
			To:      "user@example.com",
			Subject: "Welcome!",
			Body:    "Welcome to our service",
		},
		asynq.Queue("critical"),
		asynq.MaxRetry(3),
	)
	if err != nil {
		log.Fatal(err)
	}

	// Enqueue image resize task
	err = client.EnqueueImageResize(
		ImageResizePayload{
			SourceURL: "https://example.com/image.jpg",
			Width:     800,
			Height:    600,
		},
		asynq.Queue("default"),
	)
	if err != nil {
		log.Fatal(err)
	}

	// Keep the program running
	select {}
}
