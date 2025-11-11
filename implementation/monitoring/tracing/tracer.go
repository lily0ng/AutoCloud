package main

import (
	"context"
	"fmt"
	"time"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/trace"
)

type Tracer struct {
	tracer trace.Tracer
}

func NewTracer(serviceName string) *Tracer {
	return &Tracer{
		tracer: otel.Tracer(serviceName),
	}
}

func (t *Tracer) StartSpan(ctx context.Context, name string, attrs ...attribute.KeyValue) (context.Context, trace.Span) {
	return t.tracer.Start(ctx, name, trace.WithAttributes(attrs...))
}

func (t *Tracer) RecordError(span trace.Span, err error) {
	span.RecordError(err)
	span.SetAttributes(attribute.Bool("error", true))
}

func (t *Tracer) AddEvent(span trace.Span, name string, attrs ...attribute.KeyValue) {
	span.AddEvent(name, trace.WithAttributes(attrs...))
}

type TracedOperation struct {
	Name      string
	StartTime time.Time
	EndTime   time.Time
	Duration  time.Duration
	Success   bool
	Error     error
}

func (t *Tracer) TraceOperation(ctx context.Context, name string, operation func() error) *TracedOperation {
	ctx, span := t.StartSpan(ctx, name)
	defer span.End()

	op := &TracedOperation{
		Name:      name,
		StartTime: time.Now(),
	}

	err := operation()
	op.EndTime = time.Now()
	op.Duration = op.EndTime.Sub(op.StartTime)
	op.Success = err == nil
	op.Error = err

	if err != nil {
		t.RecordError(span, err)
	}

	span.SetAttributes(
		attribute.Int64("duration_ms", op.Duration.Milliseconds()),
		attribute.Bool("success", op.Success),
	)

	return op
}

func main() {
	tracer := NewTracer("example-service")
	ctx := context.Background()

	op := tracer.TraceOperation(ctx, "database-query", func() error {
		time.Sleep(100 * time.Millisecond)
		return nil
	})

	fmt.Printf("Operation: %s, Duration: %v, Success: %v\n", 
		op.Name, op.Duration, op.Success)
}
