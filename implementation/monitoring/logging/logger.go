package main

import (
	"encoding/json"
	"fmt"
	"os"
	"time"
)

type LogLevel string

const (
	DEBUG LogLevel = "DEBUG"
	INFO  LogLevel = "INFO"
	WARN  LogLevel = "WARN"
	ERROR LogLevel = "ERROR"
	FATAL LogLevel = "FATAL"
)

type LogEntry struct {
	Timestamp string                 `json:"timestamp"`
	Level     LogLevel               `json:"level"`
	Service   string                 `json:"service"`
	Message   string                 `json:"message"`
	Fields    map[string]interface{} `json:"fields,omitempty"`
}

type Logger struct {
	service string
	level   LogLevel
}

func NewLogger(service string, level LogLevel) *Logger {
	return &Logger{
		service: service,
		level:   level,
	}
}

func (l *Logger) log(level LogLevel, message string, fields map[string]interface{}) {
	entry := LogEntry{
		Timestamp: time.Now().UTC().Format(time.RFC3339),
		Level:     level,
		Service:   l.service,
		Message:   message,
		Fields:    fields,
	}

	data, err := json.Marshal(entry)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to marshal log entry: %v\n", err)
		return
	}

	fmt.Println(string(data))
}

func (l *Logger) Debug(message string, fields map[string]interface{}) {
	l.log(DEBUG, message, fields)
}

func (l *Logger) Info(message string, fields map[string]interface{}) {
	l.log(INFO, message, fields)
}

func (l *Logger) Warn(message string, fields map[string]interface{}) {
	l.log(WARN, message, fields)
}

func (l *Logger) Error(message string, fields map[string]interface{}) {
	l.log(ERROR, message, fields)
}

func (l *Logger) Fatal(message string, fields map[string]interface{}) {
	l.log(FATAL, message, fields)
	os.Exit(1)
}

func main() {
	logger := NewLogger("example-service", INFO)
	logger.Info("Service started", map[string]interface{}{
		"port": 8080,
		"env":  "production",
	})
}
