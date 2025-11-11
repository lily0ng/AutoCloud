#!/bin/bash
# Backup Automation Script
set -e
BACKUP_DIR=${BACKUP_DIR:-"/backups"}
RETENTION_DAYS=${RETENTION_DAYS:-7}
DATE=$(date +%Y%m%d_%H%M%S)

echo "🔄 Starting backup: $DATE"
mkdir -p "$BACKUP_DIR"

# Database backup
if [ -n "$DB_HOST" ]; then
    pg_dump -h "$DB_HOST" -U "$DB_USER" "$DB_NAME" > "$BACKUP_DIR/db_$DATE.sql"
    gzip "$BACKUP_DIR/db_$DATE.sql"
fi

# File backup
tar -czf "$BACKUP_DIR/files_$DATE.tar.gz" /app/data

# Cleanup old backups
find "$BACKUP_DIR" -name "*.gz" -mtime +$RETENTION_DAYS -delete

echo "✅ Backup complete"
