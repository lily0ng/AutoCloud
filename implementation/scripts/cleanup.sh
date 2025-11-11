#!/bin/bash
# Cleanup script

set -e

echo "========================================="
echo "Cleaning up AutoCloud Environment"
echo "========================================="

# Stop all containers
echo "Stopping Docker containers..."
docker-compose -f infrastructure/docker/docker-compose.yml down -v

# Clean build artifacts
echo "Cleaning build artifacts..."
rm -rf build/
rm -rf */build/
rm -rf */*.o
rm -rf coverage.*

# Clean Go cache
echo "Cleaning Go cache..."
go clean -cache -modcache -testcache

# Clean Python cache
echo "Cleaning Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete

echo "========================================="
echo "Cleanup completed!"
echo "========================================="
