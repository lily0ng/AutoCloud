#!/bin/bash
# Push all Docker images to registry

set -e

VERSION=${1:-latest}
REGISTRY=${REGISTRY:-autocloud}

echo "========================================="
echo "Pushing all Docker images"
echo "Version: $VERSION"
echo "Registry: $REGISTRY"
echo "========================================="

IMAGES=(
    "service-a"
    "service-b"
    "service-c"
    "web-app"
    "order-service"
    "nginx"
    "postgres"
    "redis"
    "kafka"
    "prometheus"
    "grafana"
)

for image in "${IMAGES[@]}"; do
    echo "Pushing $REGISTRY/$image:$VERSION..."
    docker push $REGISTRY/$image:$VERSION
done

echo ""
echo "========================================="
echo "All images pushed successfully!"
echo "========================================="
