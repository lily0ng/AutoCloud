#!/bin/bash
# Performance Benchmark Script

TARGET=${1:-http://nginx}
REQUESTS=${2:-10000}
CONCURRENCY=${3:-100}

echo "========================================="
echo "Performance Benchmark"
echo "Target: $TARGET"
echo "Requests: $REQUESTS"
echo "Concurrency: $CONCURRENCY"
echo "========================================="

# Apache Bench
echo ""
echo "Running Apache Bench..."
ab -n $REQUESTS -c $CONCURRENCY $TARGET/

# wrk
echo ""
echo "Running wrk..."
wrk -t10 -c$CONCURRENCY -d30s $TARGET/

echo ""
echo "========================================="
echo "Benchmark completed!"
echo "========================================="
