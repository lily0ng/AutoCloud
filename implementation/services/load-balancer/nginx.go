package main

import (
	"fmt"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"sync"
	"time"
)

type Backend struct {
	URL          *url.URL
	Alive        bool
	mux          sync.RWMutex
	ReverseProxy *httputil.ReverseProxy
}

type LoadBalancer struct {
	backends []*Backend
	current  int
	mux      sync.Mutex
}

func (b *Backend) SetAlive(alive bool) {
	b.mux.Lock()
	b.Alive = alive
	b.mux.Unlock()
}

func (b *Backend) IsAlive() bool {
	b.mux.RLock()
	alive := b.Alive
	b.mux.RUnlock()
	return alive
}

func NewLoadBalancer(backendURLs []string) *LoadBalancer {
	lb := &LoadBalancer{
		backends: make([]*Backend, 0),
	}

	for _, backendURL := range backendURLs {
		url, err := url.Parse(backendURL)
		if err != nil {
			log.Printf("Error parsing URL %s: %v", backendURL, err)
			continue
		}

		backend := &Backend{
			URL:          url,
			Alive:        true,
			ReverseProxy: httputil.NewSingleHostReverseProxy(url),
		}
		lb.backends = append(lb.backends, backend)
	}

	return lb
}

func (lb *LoadBalancer) GetNextBackend() *Backend {
	lb.mux.Lock()
	defer lb.mux.Unlock()

	for i := 0; i < len(lb.backends); i++ {
		idx := (lb.current + i) % len(lb.backends)
		if lb.backends[idx].IsAlive() {
			lb.current = (idx + 1) % len(lb.backends)
			return lb.backends[idx]
		}
	}
	return nil
}

func (lb *LoadBalancer) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	backend := lb.GetNextBackend()
	if backend == nil {
		http.Error(w, "No available backends", http.StatusServiceUnavailable)
		return
	}

	backend.ReverseProxy.ServeHTTP(w, r)
}

func (lb *LoadBalancer) HealthCheck() {
	ticker := time.NewTicker(30 * time.Second)
	for range ticker.C {
		for _, backend := range lb.backends {
			go func(b *Backend) {
				resp, err := http.Get(b.URL.String() + "/health")
				if err != nil || resp.StatusCode != http.StatusOK {
					b.SetAlive(false)
					log.Printf("Backend %s is down", b.URL)
				} else {
					b.SetAlive(true)
					log.Printf("Backend %s is healthy", b.URL)
				}
			}(backend)
		}
	}
}

func main() {
	backends := []string{
		"http://localhost:8080",
		"http://localhost:8081",
		"http://localhost:8082",
	}

	lb := NewLoadBalancer(backends)
	go lb.HealthCheck()

	server := http.Server{
		Addr:    ":80",
		Handler: lb,
	}

	fmt.Println("Load Balancer started on :80")
	log.Fatal(server.ListenAndServe())
}
