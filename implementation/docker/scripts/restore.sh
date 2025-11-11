#!/bin/bash
# Restore Docker volumes from backup

set -e

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

echo "========================================="
echo "Restoring from backup"
echo "File: $BACKUP_FILE"
echo "========================================="

if [[ $BACKUP_FILE == *"postgres"* ]]; then
    echo "Restoring PostgreSQL..."
    gunzip -c $BACKUP_FILE | docker exec -i autocloud-postgres psql -U admin
elif [[ $BACKUP_FILE == *"redis"* ]]; then
    echo "Restoring Redis..."
    docker cp $BACKUP_FILE autocloud-redis:/data/dump.rdb
    docker restart autocloud-redis
fi

echo ""
echo "========================================="
echo "Restore completed!"
echo "========================================="
