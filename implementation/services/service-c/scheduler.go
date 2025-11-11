package main

import (
	"context"
	"log"
	"time"
)

type Task struct {
	Name     string
	Interval time.Duration
	Execute  func() error
}

type Scheduler struct {
	tasks  []Task
	ctx    context.Context
	cancel context.CancelFunc
}

func NewScheduler() *Scheduler {
	ctx, cancel := context.WithCancel(context.Background())
	return &Scheduler{
		tasks:  make([]Task, 0),
		ctx:    ctx,
		cancel: cancel,
	}
}

func (s *Scheduler) AddTask(task Task) {
	s.tasks = append(s.tasks, task)
	log.Printf("Added task: %s (interval: %v)", task.Name, task.Interval)
}

func (s *Scheduler) Start() {
	log.Println("Scheduler started")
	for _, task := range s.tasks {
		go s.runTask(task)
	}
}

func (s *Scheduler) runTask(task Task) {
	ticker := time.NewTicker(task.Interval)
	defer ticker.Stop()

	for {
		select {
		case <-s.ctx.Done():
			log.Printf("Task %s stopped", task.Name)
			return
		case <-ticker.C:
			log.Printf("Executing task: %s", task.Name)
			if err := task.Execute(); err != nil {
				log.Printf("Task %s failed: %v", task.Name, err)
			}
		}
	}
}

func (s *Scheduler) Stop() {
	log.Println("Stopping scheduler")
	s.cancel()
}

func main() {
	scheduler := NewScheduler()

	scheduler.AddTask(Task{
		Name:     "cleanup",
		Interval: 1 * time.Hour,
		Execute: func() error {
			log.Println("Running cleanup task")
			return nil
		},
	})

	scheduler.AddTask(Task{
		Name:     "health-check",
		Interval: 30 * time.Second,
		Execute: func() error {
			log.Println("Running health check")
			return nil
		},
	})

	scheduler.Start()
	time.Sleep(5 * time.Minute)
	scheduler.Stop()
}
