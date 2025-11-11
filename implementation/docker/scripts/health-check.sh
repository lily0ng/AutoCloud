#!/bin/bash
# Check health of all Docker containers

echo "========================================="
echo "Docker Container Health Check"
echo "========================================="

docker-compose -f docker/docker-compose.yml ps

echo ""
echo "Container Health Status:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "========================================="
