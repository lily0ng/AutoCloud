# Multi-stage build for Service C
FROM golang:1.21-alpine AS builder

WORKDIR /app

COPY services/service-c/go.mod services/service-c/go.sum ./
RUN go mod download

COPY services/service-c/ ./
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o service-c .

FROM alpine:latest

RUN apk --no-cache add ca-certificates curl

WORKDIR /root/

COPY --from=builder /app/service-c .

RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /root

USER appuser

EXPOSE 8082

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8082/health || exit 1

CMD ["./service-c"]
