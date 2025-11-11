package main

import (
	"context"
	"log"
	"sync"
	"time"
)

type Job struct {
	ID      string
	Payload interface{}
}

type WorkerPool struct {
	workers    int
	jobQueue   chan Job
	results    chan interface{}
	ctx        context.Context
	cancel     context.CancelFunc
	wg         sync.WaitGroup
	processing sync.Map
}

func NewWorkerPool(workers int, queueSize int) *WorkerPool {
	ctx, cancel := context.WithCancel(context.Background())
	return &WorkerPool{
		workers:  workers,
		jobQueue: make(chan Job, queueSize),
		results:  make(chan interface{}, queueSize),
		ctx:      ctx,
		cancel:   cancel,
	}
}

func (wp *WorkerPool) Start() {
	for i := 0; i < wp.workers; i++ {
		wp.wg.Add(1)
		go wp.worker(i)
	}
	log.Printf("Started %d workers", wp.workers)
}

func (wp *WorkerPool) worker(id int) {
	defer wp.wg.Done()
	log.Printf("Worker %d started", id)

	for {
		select {
		case <-wp.ctx.Done():
			log.Printf("Worker %d stopping", id)
			return
		case job := <-wp.jobQueue:
			wp.processing.Store(job.ID, true)
			result := wp.processJob(job)
			wp.results <- result
			wp.processing.Delete(job.ID)
		}
	}
}

func (wp *WorkerPool) processJob(job Job) interface{} {
	log.Printf("Processing job %s", job.ID)
	time.Sleep(100 * time.Millisecond)
	return map[string]interface{}{
		"job_id":    job.ID,
		"status":    "completed",
		"timestamp": time.Now(),
	}
}

func (wp *WorkerPool) Submit(job Job) {
	wp.jobQueue <- job
}

func (wp *WorkerPool) Stop() {
	log.Println("Stopping worker pool")
	wp.cancel()
	close(wp.jobQueue)
	wp.wg.Wait()
	close(wp.results)
}

func (wp *WorkerPool) GetResults() <-chan interface{} {
	return wp.results
}
