# Order Service Dockerfile
FROM golang:1.21-alpine AS builder

WORKDIR /app

COPY application-layer/microservices/order-service/ ./
RUN go mod init order-service && \
    go mod tidy && \
    CGO_ENABLED=0 GOOS=linux go build -o order-service .

FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/

COPY --from=builder /app/order-service .

RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /root

USER appuser

EXPOSE 8083

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget --spider http://localhost:8083/api/v1/orders || exit 1

CMD ["./order-service"]
