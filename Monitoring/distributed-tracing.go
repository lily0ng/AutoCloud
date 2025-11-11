package main
import ("fmt"; "log"; "time")
type Span struct {TraceID string; SpanID string; ParentID string; Operation string; StartTime time.Time; Duration time.Duration; Tags map[string]string}
type Tracer struct {traces map[string][]Span}
func NewTracer() *Tracer {return &Tracer{traces: make(map[string][]Span)}}
func (t *Tracer) StartSpan(traceID, operation string) *Span {
	span := &Span{TraceID: traceID, SpanID: fmt.Sprintf("span-%d", time.Now().UnixNano()), Operation: operation, StartTime: time.Now(), Tags: make(map[string]string)}
	log.Printf("🔍 Span started: %s", operation)
	return span
}
func (t *Tracer) FinishSpan(span *Span) {
	span.Duration = time.Since(span.StartTime)
	t.traces[span.TraceID] = append(t.traces[span.TraceID], *span)
	log.Printf("✅ Span finished: %s (%.2fms)", span.Operation, float64(span.Duration.Microseconds())/1000)
}
func main() {
	tracer := NewTracer()
	span := tracer.StartSpan("trace-1", "http.request")
	time.Sleep(50 * time.Millisecond)
	tracer.FinishSpan(span)
	fmt.Println("✅ Distributed tracing active")
}
