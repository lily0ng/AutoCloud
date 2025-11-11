#!/bin/bash
# RDS Automated Backup Scheduler

set -e

DB_INSTANCE_ID=${1:-autocloud-db}
BACKUP_RETENTION=${2:-7}

echo "========================================="
echo "RDS Backup Scheduler"
echo "DB Instance: $DB_INSTANCE_ID"
echo "Retention Days: $BACKUP_RETENTION"
echo "========================================="

# Enable automated backups
echo "Enabling automated backups..."
aws rds modify-db-instance \
    --db-instance-identifier $DB_INSTANCE_ID \
    --backup-retention-period $BACKUP_RETENTION \
    --preferred-backup-window "03:00-04:00" \
    --apply-immediately

# Create manual snapshot
SNAPSHOT_ID="${DB_INSTANCE_ID}-manual-$(date +%Y%m%d-%H%M%S)"
echo "Creating manual snapshot: $SNAPSHOT_ID"
aws rds create-db-snapshot \
    --db-instance-identifier $DB_INSTANCE_ID \
    --db-snapshot-identifier $SNAPSHOT_ID

# Wait for snapshot to complete
echo "Waiting for snapshot to complete..."
aws rds wait db-snapshot-completed \
    --db-snapshot-identifier $SNAPSHOT_ID

# List recent snapshots
echo ""
echo "Recent snapshots:"
aws rds describe-db-snapshots \
    --db-instance-identifier $DB_INSTANCE_ID \
    --query 'DBSnapshots[*].[DBSnapshotIdentifier,SnapshotCreateTime,Status]' \
    --output table

# Clean old manual snapshots (keep last 5)
echo ""
echo "Cleaning old snapshots..."
aws rds describe-db-snapshots \
    --db-instance-identifier $DB_INSTANCE_ID \
    --snapshot-type manual \
    --query 'DBSnapshots[*].DBSnapshotIdentifier' \
    --output text | tr '\t' '\n' | tail -n +6 | while read snapshot; do
    echo "Deleting old snapshot: $snapshot"
    aws rds delete-db-snapshot --db-snapshot-identifier $snapshot
done

echo ""
echo "========================================="
echo "Backup scheduling completed!"
echo "========================================="
