#!/bin/bash
# Setup Docker Registry

set -e

mkdir -p auth

echo "Creating registry authentication..."
docker run --rm --entrypoint htpasswd \
    httpd:2 -Bbn admin changeme > auth/htpasswd

echo "Starting registry..."
docker-compose -f docker-compose.registry.yml up -d

echo ""
echo "========================================="
echo "Docker Registry is running!"
echo "Registry: http://localhost:5000"
echo "UI: http://localhost:8081"
echo "Username: admin"
echo "Password: changeme"
echo "========================================="
