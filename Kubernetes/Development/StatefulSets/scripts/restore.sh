#!/bin/bash

# Set environment variables
NAMESPACE="default"

# Check if backup file is provided
if [ -z "$1" ]; then
    echo "Please provide the backup file path"
    echo "Usage: ./restore.sh <backup_file_path>"
    exit 1
fi

# Validate backup file exists
if [ ! -f "$1" ]; then
    echo "Backup file not found: $1"
    exit 1
fi

# Restore from backup
echo "Restoring from backup: $1"
kubectl apply -f "$1" -n ${NAMESPACE}

echo "Restore completed successfully!"
