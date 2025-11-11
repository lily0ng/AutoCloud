#!/bin/bash
# Automated Backup Script

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/backups

mkdir -p $BACKUP_DIR

echo "Starting backup at $TIMESTAMP..."

# Backup PostgreSQL
pg_dump -h postgres -U admin appdb | gzip > $BACKUP_DIR/postgres_$TIMESTAMP.sql.gz

# Backup Redis
redis-cli -h redis --rdb $BACKUP_DIR/redis_$TIMESTAMP.rdb

# Upload to S3 (if configured)
if [ -n "$AWS_S3_BUCKET" ]; then
    aws s3 cp $BACKUP_DIR/ s3://$AWS_S3_BUCKET/backups/ --recursive
fi

echo "Backup completed!"
