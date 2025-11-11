#!/bin/bash
# Deployment script for AutoCloud

set -e

echo "🚀 Starting AutoCloud deployment..."

# Configuration
ENVIRONMENT=${1:-production}
VERSION=${2:-latest}
DEPLOY_DIR="/opt/autocloud"

echo "📦 Environment: $ENVIRONMENT"
echo "📦 Version: $VERSION"

# Pull latest code
echo "📥 Pulling latest code..."
git pull origin main

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️  Running database migrations..."
alembic upgrade head

# Build assets
echo "🏗️  Building assets..."
npm run build

# Run tests
echo "🧪 Running tests..."
pytest tests/

# Restart services
echo "🔄 Restarting services..."
systemctl restart autocloud-api
systemctl restart autocloud-worker

# Health check
echo "🏥 Running health check..."
curl -f http://localhost:8000/health || exit 1

echo "✅ Deployment completed successfully!"
