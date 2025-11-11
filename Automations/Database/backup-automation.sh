#!/bin/bash
# Database Backup Automation

set -e

BACKUP_DIR="/var/backups/database"
RETENTION_DAYS=7
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

backup_mysql() {
    local db_name=$1
    local backup_file="$BACKUP_DIR/mysql_${db_name}_${DATE}.sql.gz"
    
    echo "📦 Backing up MySQL database: $db_name"
    mysqldump -u root -p"$MYSQL_PASSWORD" "$db_name" | gzip > "$backup_file"
    echo "✅ Backup created: $backup_file"
}

backup_postgresql() {
    local db_name=$1
    local backup_file="$BACKUP_DIR/postgres_${db_name}_${DATE}.sql.gz"
    
    echo "📦 Backing up PostgreSQL database: $db_name"
    pg_dump -U postgres "$db_name" | gzip > "$backup_file"
    echo "✅ Backup created: $backup_file"
}

backup_mongodb() {
    local db_name=$1
    local backup_dir="$BACKUP_DIR/mongo_${db_name}_${DATE}"
    
    echo "📦 Backing up MongoDB database: $db_name"
    mongodump --db "$db_name" --out "$backup_dir"
    tar -czf "${backup_dir}.tar.gz" -C "$BACKUP_DIR" "$(basename $backup_dir)"
    rm -rf "$backup_dir"
    echo "✅ Backup created: ${backup_dir}.tar.gz"
}

cleanup_old_backups() {
    echo "🧹 Cleaning up backups older than $RETENTION_DAYS days..."
    find "$BACKUP_DIR" -name "*.gz" -mtime +$RETENTION_DAYS -delete
    echo "✅ Cleanup complete"
}

upload_to_s3() {
    local backup_file=$1
    local s3_bucket=${S3_BUCKET:-"my-db-backups"}
    
    if command -v aws &> /dev/null; then
        echo "☁️  Uploading to S3: $s3_bucket"
        aws s3 cp "$backup_file" "s3://$s3_bucket/$(basename $backup_file)"
        echo "✅ Upload complete"
    fi
}

case "${1:-mysql}" in
    mysql)
        backup_mysql "${2:-mydb}"
        ;;
    postgres)
        backup_postgresql "${2:-mydb}"
        ;;
    mongodb)
        backup_mongodb "${2:-mydb}"
        ;;
    cleanup)
        cleanup_old_backups
        ;;
    *)
        echo "Usage: $0 {mysql|postgres|mongodb|cleanup} [database_name]"
        exit 1
        ;;
esac
