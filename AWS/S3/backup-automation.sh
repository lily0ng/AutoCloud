#!/bin/bash
# S3 Backup Automation Script

set -e

SOURCE_BUCKET=${1:-source-bucket}
BACKUP_BUCKET=${2:-backup-bucket}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "========================================="
echo "S3 Backup Automation"
echo "Source: $SOURCE_BUCKET"
echo "Backup: $BACKUP_BUCKET"
echo "Timestamp: $TIMESTAMP"
echo "========================================="

# Create backup directory
BACKUP_PREFIX="backups/$TIMESTAMP"

# Sync source to backup
echo "Syncing $SOURCE_BUCKET to $BACKUP_BUCKET/$BACKUP_PREFIX..."
aws s3 sync s3://$SOURCE_BUCKET s3://$BACKUP_BUCKET/$BACKUP_PREFIX \
    --storage-class STANDARD_IA \
    --metadata "backup-date=$TIMESTAMP"

# Verify backup
OBJECT_COUNT=$(aws s3 ls s3://$BACKUP_BUCKET/$BACKUP_PREFIX --recursive | wc -l)
echo "Backed up $OBJECT_COUNT objects"

# Clean old backups (keep last 7 days)
echo "Cleaning old backups..."
CUTOFF_DATE=$(date -d '7 days ago' +%Y%m%d)

aws s3 ls s3://$BACKUP_BUCKET/backups/ | while read -r line; do
    BACKUP_DATE=$(echo $line | awk '{print $2}' | cut -d'_' -f1 | tr -d '/')
    if [[ $BACKUP_DATE < $CUTOFF_DATE ]]; then
        BACKUP_DIR=$(echo $line | awk '{print $2}')
        echo "Deleting old backup: $BACKUP_DIR"
        aws s3 rm s3://$BACKUP_BUCKET/backups/$BACKUP_DIR --recursive
    fi
done

echo "Backup completed successfully!"
