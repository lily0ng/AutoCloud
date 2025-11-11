interface Span {traceId: string; spanId: string; operation: string; duration: number}
class TracingService {
  traces: Span[] = [];
  startSpan(operation: string): Span {
    const span = {traceId: 'trace-1', spanId: `span-${this.traces.length}`, operation, duration: 0};
    this.traces.push(span);
    console.log(`🔍 Span started: ${operation}`);
    return span;
  }
}
const tracer = new TracingService();
tracer.startSpan('http.request');
