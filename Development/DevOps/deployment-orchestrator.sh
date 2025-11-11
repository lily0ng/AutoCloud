#!/bin/bash
# Deployment Orchestrator
APP=${1:-"web-app"}
ENV=${2:-"production"}
VERSION=${3:-"latest"}

echo "🚀 Deploying $APP to $ENV (version: $VERSION)"
echo "  Updating deployment..."
kubectl set image deployment/$APP $APP=$APP:$VERSION -n $ENV
echo "  Waiting for rollout..."
kubectl rollout status deployment/$APP -n $ENV
echo "  Verifying health..."
kubectl get pods -n $ENV -l app=$APP
echo "✅ Deployment complete!"
