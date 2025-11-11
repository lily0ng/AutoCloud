#!/bin/bash
# Rolling Update Script

set -e

SERVICE_NAME=$1
NEW_VERSION=$2
NAMESPACE=${3:-production}
MAX_UNAVAILABLE=1

if [ -z "$SERVICE_NAME" ] || [ -z "$NEW_VERSION" ]; then
    echo "Usage: $0 <service-name> <version> [namespace]"
    exit 1
fi

echo "========================================="
echo "Rolling Update: $SERVICE_NAME"
echo "Version: $NEW_VERSION"
echo "Namespace: $NAMESPACE"
echo "========================================="

# Get current replicas
REPLICAS=$(kubectl get deployment $SERVICE_NAME -n $NAMESPACE -o jsonpath='{.spec.replicas}')
echo "Current replicas: $REPLICAS"

# Update image
echo "Updating image..."
kubectl set image deployment/$SERVICE_NAME \
    $SERVICE_NAME=autocloud/$SERVICE_NAME:$NEW_VERSION \
    -n $NAMESPACE

# Monitor rollout
echo "Monitoring rollout..."
kubectl rollout status deployment/$SERVICE_NAME -n $NAMESPACE --timeout=5m

# Verify deployment
echo "Verifying deployment..."
READY_REPLICAS=$(kubectl get deployment $SERVICE_NAME -n $NAMESPACE -o jsonpath='{.status.readyReplicas}')

if [ "$READY_REPLICAS" -eq "$REPLICAS" ]; then
    echo "✓ Deployment successful: $READY_REPLICAS/$REPLICAS replicas ready"
else
    echo "✗ Deployment failed: Only $READY_REPLICAS/$REPLICAS replicas ready"
    echo "Rolling back..."
    kubectl rollout undo deployment/$SERVICE_NAME -n $NAMESPACE
    exit 1
fi

echo "========================================="
echo "Rolling Update Completed Successfully"
echo "========================================="
