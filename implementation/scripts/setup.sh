#!/bin/bash
# Setup script for development environment

set -e

echo "========================================="
echo "Setting up AutoCloud Development Environment"
echo "========================================="

# Check prerequisites
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "Error: $1 is not installed"
        exit 1
    fi
}

echo "Checking prerequisites..."
check_command go
check_command python3
check_command docker
check_command kubectl

# Install Go dependencies
echo "Installing Go dependencies..."
cd services/service-a && go mod download && cd -
cd services/service-b && go mod download && cd -
cd services/service-c && go mod download && cd -

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Setup database
echo "Setting up database..."
docker-compose -f infrastructure/docker/docker-compose.yml up -d postgres
sleep 5
psql -h localhost -U admin -d appdb -f database/migrations/001_init.sql

# Setup Redis
echo "Setting up Redis..."
docker-compose -f infrastructure/docker/docker-compose.yml up -d redis

# Setup Kafka
echo "Setting up Kafka..."
docker-compose -f infrastructure/docker/docker-compose.yml up -d kafka zookeeper

echo "========================================="
echo "Setup completed successfully!"
echo "Run 'docker-compose up' to start all services"
echo "========================================="
