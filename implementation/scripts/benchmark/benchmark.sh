#!/bin/bash
# Benchmark Script

set -e

SERVICES=(
    "http://localhost:8080/health"
    "http://localhost:8081/health"
    "http://localhost:8082/health"
)

REQUESTS=1000
CONCURRENCY=10

echo "========================================="
echo "Performance Benchmark"
echo "========================================="

for service in "${SERVICES[@]}"; do
    echo ""
    echo "Benchmarking: $service"
    echo "Requests: $REQUESTS, Concurrency: $CONCURRENCY"
    echo ""
    
    if command -v ab &> /dev/null; then
        ab -n $REQUESTS -c $CONCURRENCY "$service"
    elif command -v wrk &> /dev/null; then
        wrk -t$CONCURRENCY -c$CONCURRENCY -d10s "$service"
    else
        echo "No benchmark tool found (ab or wrk)"
    fi
    
    echo "---"
done

echo ""
echo "========================================="
echo "Benchmark Completed"
echo "========================================="
