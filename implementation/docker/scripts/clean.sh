#!/bin/bash
# Clean Docker resources

set -e

echo "========================================="
echo "Cleaning Docker resources"
echo "========================================="

# Stop all containers
echo "Stopping containers..."
docker-compose -f docker/docker-compose.yml down

# Remove unused images
echo "Removing unused images..."
docker image prune -f

# Remove unused volumes
echo "Removing unused volumes..."
docker volume prune -f

# Remove unused networks
echo "Removing unused networks..."
docker network prune -f

# Remove build cache
echo "Removing build cache..."
docker builder prune -f

echo ""
echo "========================================="
echo "Cleanup completed!"
echo "========================================="
