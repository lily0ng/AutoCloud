#!/bin/bash
# Backup Scheduler

set -e

BACKUP_DIR="/var/backups"
RETENTION_DAYS=7

schedule_backup() {
    local cron_schedule=$1
    local backup_script=$2
    
    echo "Scheduling backup: $cron_schedule"
    
    (crontab -l 2>/dev/null; echo "$cron_schedule $backup_script") | crontab -
    
    echo "✅ Backup scheduled"
}

backup_files() {
    local source=$1
    local name=$(basename "$source")
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$BACKUP_DIR/${name}_${timestamp}.tar.gz"
    
    mkdir -p "$BACKUP_DIR"
    
    echo "Backing up $source..."
    tar -czf "$backup_file" "$source"
    
    echo "✅ Backup created: $backup_file"
}

backup_database() {
    local db_name=$1
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$BACKUP_DIR/${db_name}_${timestamp}.sql.gz"
    
    mkdir -p "$BACKUP_DIR"
    
    echo "Backing up database: $db_name..."
    mysqldump "$db_name" | gzip > "$backup_file"
    
    echo "✅ Database backup created: $backup_file"
}

cleanup_old_backups() {
    echo "Cleaning up backups older than $RETENTION_DAYS days..."
    find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
    find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete
    echo "✅ Cleanup complete"
}

case "${1:-schedule}" in
    schedule)
        schedule_backup "$2" "$3"
        ;;
    backup-files)
        backup_files "$2"
        ;;
    backup-db)
        backup_database "$2"
        ;;
    cleanup)
        cleanup_old_backups
        ;;
esac
