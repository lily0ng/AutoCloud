#!/bin/bash

# Set environment variables
NAMESPACE="default"
APP_NAME="app-statefulset"

# Check if replicas argument is provided
if [ -z "$1" ]; then
    echo "Please provide the number of replicas"
    echo "Usage: ./scale.sh <number_of_replicas>"
    exit 1
fi

# Scale the StatefulSet
echo "Scaling StatefulSet to $1 replicas..."
kubectl scale statefulset ${APP_NAME} --replicas=$1 -n ${NAMESPACE}

# Wait for scaling to complete
echo "Waiting for scaling operation to complete..."
kubectl rollout status statefulset/${APP_NAME} -n ${NAMESPACE}

echo "Scaling completed successfully!"
