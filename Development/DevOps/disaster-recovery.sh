#!/bin/bash
# Disaster Recovery Script
set -e

echo "🚨 Starting disaster recovery..."

# Restore from latest backup
LATEST_DB=$(ls -t /backups/db_*.sql.gz | head -1)
LATEST_FILES=$(ls -t /backups/files_*.tar.gz | head -1)

if [ -n "$LATEST_DB" ]; then
    gunzip -c "$LATEST_DB" | psql -h "$DB_HOST" -U "$DB_USER" "$DB_NAME"
fi

if [ -n "$LATEST_FILES" ]; then
    tar -xzf "$LATEST_FILES" -C /
fi

echo "✅ Recovery complete"
