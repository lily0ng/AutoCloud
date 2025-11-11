#!/bin/bash
# Build all Docker images

set -e

VERSION=${1:-latest}
REGISTRY=${REGISTRY:-autocloud}

echo "========================================="
echo "Building all Docker images"
echo "Version: $VERSION"
echo "Registry: $REGISTRY"
echo "========================================="

# Build services
echo "Building service-a..."
docker build -t $REGISTRY/service-a:$VERSION -f docker/services/service-a/Dockerfile .

echo "Building service-b..."
docker build -t $REGISTRY/service-b:$VERSION -f docker/services/service-b/Dockerfile .

echo "Building service-c..."
docker build -t $REGISTRY/service-c:$VERSION -f docker/services/service-c/Dockerfile .

echo "Building web-app..."
docker build -t $REGISTRY/web-app:$VERSION -f docker/services/web-app/Dockerfile .

echo "Building order-service..."
docker build -t $REGISTRY/order-service:$VERSION -f docker/services/order-service/Dockerfile .

# Build infrastructure
echo "Building nginx..."
docker build -t $REGISTRY/nginx:$VERSION -f docker/nginx/Dockerfile .

echo "Building postgres..."
docker build -t $REGISTRY/postgres:$VERSION -f docker/postgres/Dockerfile .

echo "Building redis..."
docker build -t $REGISTRY/redis:$VERSION -f docker/redis/Dockerfile .

echo "Building kafka..."
docker build -t $REGISTRY/kafka:$VERSION -f docker/kafka/Dockerfile .

# Build monitoring
echo "Building prometheus..."
docker build -t $REGISTRY/prometheus:$VERSION -f docker/prometheus/Dockerfile .

echo "Building grafana..."
docker build -t $REGISTRY/grafana:$VERSION -f docker/grafana/Dockerfile .

echo ""
echo "========================================="
echo "All images built successfully!"
echo "========================================="
docker images | grep $REGISTRY
