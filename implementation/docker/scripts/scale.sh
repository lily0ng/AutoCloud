#!/bin/bash
# Scale Docker services

SERVICE=$1
REPLICAS=$2

if [ -z "$SERVICE" ] || [ -z "$REPLICAS" ]; then
    echo "Usage: $0 <service> <replicas>"
    exit 1
fi

echo "Scaling $SERVICE to $REPLICAS replicas..."
docker-compose -f docker/docker-compose.yml up -d --scale $SERVICE=$REPLICAS

echo "Current status:"
docker-compose -f docker/docker-compose.yml ps $SERVICE
