#!/bin/bash

# Set environment variables
NAMESPACE="default"
APP_NAME="app-statefulset"

# Create namespace if it doesn't exist
kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

# Apply configurations
echo "Applying StatefulSet configurations..."
kubectl apply -f ../manifests/headless-service.yaml -n ${NAMESPACE}
kubectl apply -f ../manifests/statefulset.yaml -n ${NAMESPACE}

# Wait for StatefulSet to be ready
echo "Waiting for StatefulSet to be ready..."
kubectl rollout status statefulset/${APP_NAME} -n ${NAMESPACE}

echo "Deployment completed successfully!"
