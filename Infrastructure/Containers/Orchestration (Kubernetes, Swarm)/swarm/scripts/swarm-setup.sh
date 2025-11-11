#!/usr/bin/env bash

# Safer strict mode
set -euo pipefail
trap 'echo "Error on line $LINENO" >&2' ERR

echo "Starting Docker Swarm setup..."

# Check Docker CLI available
if ! command -v docker >/dev/null 2>&1; then
    echo "docker CLI not found. Please install Docker and ensure it's running." >&2
    exit 1
fi

# Initialize Swarm if not active
if ! docker info 2>/dev/null | grep -q "Swarm: active"; then
    echo "Initializing Docker Swarm..."
    docker swarm init
else
    echo "Swarm is already initialized"
fi

# Create overlay network (idempotent)
echo "Creating overlay network..."
if ! docker network inspect app-network >/dev/null 2>&1; then
    docker network create --driver overlay --attachable app-network
else
    echo "Network 'app-network' already exists"
fi

# Deploy monitoring stack (verify compose file exists)
COMPOSE_FILE="$(dirname "$0")/../configs/docker-compose.yaml"
echo "Deploying monitoring stack..."
if [[ -f "$COMPOSE_FILE" ]]; then
    docker stack deploy -c "$COMPOSE_FILE" app-stack
else
    echo "Compose file not found at $COMPOSE_FILE; skipping stack deploy" >&2
fi

# Create required directories (idempotent)
echo "Creating required directories..."
mkdir -p /app/data || true
mkdir -p /data/redis || true

# Set up node labels (only if NodeID is available)
echo "Setting up node labels..."
NODE_ID=$(docker info -f '{{.Swarm.NodeID}}' 2>/dev/null || true)
if [[ -n "$NODE_ID" ]]; then
    docker node update --label-add environment=production "$NODE_ID"
else
    echo "Node ID not available (not a swarm manager or Docker not running as manager); skipping node label updates"
fi

echo "Swarm setup complete!"
echo "To view services, run: docker service ls"
echo "To view tasks, run: docker stack ps app-stack"
