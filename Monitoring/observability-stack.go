package main

import (
	"fmt"
	"log"
	"time"
)

type Metric struct {
	Name      string
	Value     float64
	Labels    map[string]string
	Timestamp time.Time
}

type Log struct {
	Level     string
	Message   string
	Service   string
	Timestamp time.Time
	Fields    map[string]interface{}
}

type Trace struct {
	TraceID   string
	SpanID    string
	Operation string
	Duration  time.Duration
	Tags      map[string]string
}

type ObservabilityStack struct {
	metrics []Metric
	logs    []Log
	traces  []Trace
}

func NewObservabilityStack() *ObservabilityStack {
	return &ObservabilityStack{
		metrics: make([]Metric, 0),
		logs:    make([]Log, 0),
		traces:  make([]Trace, 0),
	}
}

func (os *ObservabilityStack) RecordMetric(metric Metric) {
	metric.Timestamp = time.Now()
	os.metrics = append(os.metrics, metric)
	log.Printf("📊 Metric recorded: %s = %.2f", metric.Name, metric.Value)
}

func (os *ObservabilityStack) LogEvent(logEntry Log) {
	logEntry.Timestamp = time.Now()
	os.logs = append(os.logs, logEntry)
	log.Printf("📝 Log: [%s] %s - %s", logEntry.Level, logEntry.Service, logEntry.Message)
}

func (os *ObservabilityStack) RecordTrace(trace Trace) {
	os.traces = append(os.traces, trace)
	log.Printf("🔍 Trace: %s - %s (%.2fms)", trace.TraceID, trace.Operation, float64(trace.Duration.Microseconds())/1000)
}

func (os *ObservabilityStack) QueryMetrics(name string, since time.Duration) []Metric {
	cutoff := time.Now().Add(-since)
	results := make([]Metric, 0)
	
	for _, m := range os.metrics {
		if m.Name == name && m.Timestamp.After(cutoff) {
			results = append(results, m)
		}
	}
	
	return results
}

func (os *ObservabilityStack) SearchLogs(service string, level string) []Log {
	results := make([]Log, 0)
	
	for _, l := range os.logs {
		if (service == "" || l.Service == service) && (level == "" || l.Level == level) {
			results = append(results, l)
		}
	}
	
	return results
}

func (os *ObservabilityStack) AnalyzePerformance() {
	fmt.Println("\n📈 Performance Analysis:")
	
	// Analyze traces
	if len(os.traces) > 0 {
		var totalDuration time.Duration
		for _, t := range os.traces {
			totalDuration += t.Duration
		}
		avgDuration := totalDuration / time.Duration(len(os.traces))
		fmt.Printf("  Avg Request Duration: %.2fms\n", float64(avgDuration.Microseconds())/1000)
	}
	
	// Analyze logs
	errorCount := 0
	for _, l := range os.logs {
		if l.Level == "ERROR" {
			errorCount++
		}
	}
	if len(os.logs) > 0 {
		fmt.Printf("  Error Rate: %.2f%%\n", float64(errorCount)/float64(len(os.logs))*100)
	}
	
	// Analyze metrics
	fmt.Printf("  Total Metrics: %d\n", len(os.metrics))
	fmt.Printf("  Total Logs: %d\n", len(os.logs))
	fmt.Printf("  Total Traces: %d\n", len(os.traces))
}

func main() {
	stack := NewObservabilityStack()
	
	// Record metrics
	stack.RecordMetric(Metric{
		Name:  "http_requests_total",
		Value: 1250,
		Labels: map[string]string{
			"method": "GET",
			"status": "200",
		},
	})
	
	stack.RecordMetric(Metric{
		Name:  "cpu_usage_percent",
		Value: 45.5,
		Labels: map[string]string{
			"host": "web-server-1",
		},
	})
	
	// Log events
	stack.LogEvent(Log{
		Level:   "INFO",
		Message: "Application started",
		Service: "web-api",
		Fields: map[string]interface{}{
			"port": 8080,
			"env":  "production",
		},
	})
	
	stack.LogEvent(Log{
		Level:   "ERROR",
		Message: "Database connection failed",
		Service: "web-api",
		Fields: map[string]interface{}{
			"error": "connection timeout",
		},
	})
	
	// Record traces
	stack.RecordTrace(Trace{
		TraceID:   "trace-123",
		SpanID:    "span-456",
		Operation: "GET /api/users",
		Duration:  45 * time.Millisecond,
		Tags: map[string]string{
			"http.method": "GET",
			"http.status": "200",
		},
	})
	
	// Query and analyze
	cpuMetrics := stack.QueryMetrics("cpu_usage_percent", 1*time.Hour)
	fmt.Printf("\n📊 CPU metrics in last hour: %d\n", len(cpuMetrics))
	
	errorLogs := stack.SearchLogs("", "ERROR")
	fmt.Printf("🚨 Error logs: %d\n", len(errorLogs))
	
	stack.AnalyzePerformance()
	
	fmt.Println("\n✅ Observability stack operational")
}
