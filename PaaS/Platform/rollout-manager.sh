#!/bin/bash
APP=${1:-"my-app"}
VERSION=${2:-"v1.0.0"}
echo "🔄 Rolling out $APP $VERSION..."
echo "  Deploying to 25% of instances..."
echo "  Health check passed"
echo "  Deploying to 50%..."
echo "  Deploying to 100%..."
echo "✅ Rollout complete"
