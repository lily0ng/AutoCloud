#!/bin/bash
# Backup Docker volumes

set -e

BACKUP_DIR=${BACKUP_DIR:-./backups}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

echo "========================================="
echo "Backing up Docker volumes"
echo "========================================="

# Backup PostgreSQL
echo "Backing up PostgreSQL..."
docker exec autocloud-postgres pg_dumpall -U admin | gzip > $BACKUP_DIR/postgres_$TIMESTAMP.sql.gz

# Backup Redis
echo "Backing up Redis..."
docker exec autocloud-redis redis-cli --rdb /data/dump.rdb
docker cp autocloud-redis:/data/dump.rdb $BACKUP_DIR/redis_$TIMESTAMP.rdb

echo ""
echo "========================================="
echo "Backups completed!"
echo "Location: $BACKUP_DIR"
echo "========================================="
ls -lh $BACKUP_DIR
