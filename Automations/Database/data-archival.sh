#!/bin/bash
# Database Data Archival

set -e

ARCHIVE_DIR="/var/archives/database"
ARCHIVE_AGE_DAYS=90

mkdir -p "$ARCHIVE_DIR"

archive_old_data() {
    local db_name=$1
    local table=$2
    local date_column=${3:-created_at}
    local cutoff_date=$(date -d "$ARCHIVE_AGE_DAYS days ago" +%Y-%m-%d)
    
    echo "📦 Archiving data older than $cutoff_date from $table..."
    
    local archive_file="$ARCHIVE_DIR/${table}_$(date +%Y%m%d).sql.gz"
    
    # Export old data
    mysql -u root -p"$MYSQL_PASSWORD" "$db_name" -e \
        "SELECT * FROM $table WHERE $date_column < '$cutoff_date'" \
        | gzip > "$archive_file"
    
    # Delete old data
    mysql -u root -p"$MYSQL_PASSWORD" "$db_name" -e \
        "DELETE FROM $table WHERE $date_column < '$cutoff_date'"
    
    echo "✅ Archived to: $archive_file"
}

archive_postgresql_data() {
    local db_name=$1
    local table=$2
    local date_column=${3:-created_at}
    local cutoff_date=$(date -d "$ARCHIVE_AGE_DAYS days ago" +%Y-%m-%d)
    
    echo "📦 Archiving PostgreSQL data..."
    
    local archive_file="$ARCHIVE_DIR/${table}_$(date +%Y%m%d).sql.gz"
    
    psql -U postgres -d "$db_name" -c \
        "COPY (SELECT * FROM $table WHERE $date_column < '$cutoff_date') TO STDOUT" \
        | gzip > "$archive_file"
    
    psql -U postgres -d "$db_name" -c \
        "DELETE FROM $table WHERE $date_column < '$cutoff_date'"
    
    echo "✅ Archived to: $archive_file"
}

list_archives() {
    echo "📋 Available archives:"
    ls -lh "$ARCHIVE_DIR"
}

restore_archive() {
    local archive_file=$1
    
    echo "🔄 Restoring from archive: $archive_file..."
    
    gunzip -c "$archive_file" | mysql -u root -p"$MYSQL_PASSWORD"
    
    echo "✅ Restore complete"
}

case "${1:-list}" in
    archive-mysql)
        archive_old_data "$2" "$3" "$4"
        ;;
    archive-postgres)
        archive_postgresql_data "$2" "$3" "$4"
        ;;
    list)
        list_archives
        ;;
    restore)
        restore_archive "$2"
        ;;
esac
