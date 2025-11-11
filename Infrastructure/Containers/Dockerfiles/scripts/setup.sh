#!/bin/bash

# Setup script for infrastructure configuration

# Exit on error
set -e

echo "Starting infrastructure setup..."

# Create necessary directories
mkdir -p /app/data/config
mkdir -p /app/data/logs

# Set permissions
chmod 755 /app/data/config
chmod 755 /app/data/logs

# Initialize configuration
echo "Initializing configuration..."
if [ ! -f /app/data/config/config.yaml ]; then
    echo "Creating default configuration..."
    cat > /app/data/config/config.yaml << EOF
environment: development
logging:
  level: INFO
  path: /app/data/logs
settings:
  auto_update: true
  backup_enabled: true
EOF
fi

echo "Setup completed successfully!"
 