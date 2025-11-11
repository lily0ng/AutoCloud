#!/bin/bash
# Rollback Tool
set -e

DEPLOYMENT=${DEPLOYMENT:-"myapp"}
NAMESPACE=${NAMESPACE:-"default"}

echo "⏪ Rolling back deployment: $DEPLOYMENT"

kubectl rollout undo deployment/"$DEPLOYMENT" -n "$NAMESPACE"
kubectl rollout status deployment/"$DEPLOYMENT" -n "$NAMESPACE"

echo "✅ Rollback complete"
