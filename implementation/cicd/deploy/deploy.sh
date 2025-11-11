#!/bin/bash
# Deployment Script for CI/CD Pipeline

set -e

ENVIRONMENT=${1:-dev}
VERSION=${2:-latest}

echo "========================================="
echo "Deploying to $ENVIRONMENT environment"
echo "Version: $VERSION"
echo "========================================="

case $ENVIRONMENT in
    dev)
        NAMESPACE="development"
        REPLICAS=1
        ;;
    staging)
        NAMESPACE="staging"
        REPLICAS=2
        ;;
    prod)
        NAMESPACE="production"
        REPLICAS=3
        ;;
    *)
        echo "Invalid environment: $ENVIRONMENT"
        exit 1
        ;;
esac

# Build Docker images
echo "Building Docker images..."
docker build -t autocloud/service-a:$VERSION services/service-a/
docker build -t autocloud/service-b:$VERSION services/service-b/
docker build -t autocloud/service-c:$VERSION services/service-c/

# Push to registry
echo "Pushing images to registry..."
docker push autocloud/service-a:$VERSION
docker push autocloud/service-b:$VERSION
docker push autocloud/service-c:$VERSION

# Deploy to Kubernetes
echo "Deploying to Kubernetes..."
kubectl set image deployment/service-a service-a=autocloud/service-a:$VERSION -n $NAMESPACE
kubectl set image deployment/service-b service-b=autocloud/service-b:$VERSION -n $NAMESPACE
kubectl set image deployment/service-c service-c=autocloud/service-c:$VERSION -n $NAMESPACE

# Wait for rollout
echo "Waiting for rollout to complete..."
kubectl rollout status deployment/service-a -n $NAMESPACE
kubectl rollout status deployment/service-b -n $NAMESPACE
kubectl rollout status deployment/service-c -n $NAMESPACE

echo "========================================="
echo "Deployment completed successfully!"
echo "========================================="
