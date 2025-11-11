#!/bin/bash
# Backup script for AutoCloud

set -e

echo "💾 Starting backup process..."

# Configuration
BACKUP_DIR="/var/backups/autocloud"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_NAME="autocloud"
S3_BUCKET="autocloud-backups"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
echo "🗄️  Backing up database..."
pg_dump $DB_NAME | gzip > $BACKUP_DIR/db_$TIMESTAMP.sql.gz

# Backup application data
echo "📁 Backing up application data..."
tar -czf $BACKUP_DIR/data_$TIMESTAMP.tar.gz /opt/autocloud/data

# Upload to S3
echo "☁️  Uploading to S3..."
aws s3 cp $BACKUP_DIR/db_$TIMESTAMP.sql.gz s3://$S3_BUCKET/
aws s3 cp $BACKUP_DIR/data_$TIMESTAMP.tar.gz s3://$S3_BUCKET/

# Cleanup old backups (keep last 7 days)
echo "🧹 Cleaning up old backups..."
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "✅ Backup completed successfully!"
