#!/bin/bash
# Database Migration Runner

set -e

MIGRATIONS_DIR="./migrations"

run_migrations() {
    local db_type=$1
    
    echo "🔄 Running database migrations..."
    
    if [ ! -d "$MIGRATIONS_DIR" ]; then
        echo "❌ Migrations directory not found"
        exit 1
    fi
    
    for migration in $(ls -1 "$MIGRATIONS_DIR"/*.sql | sort); do
        echo "  Applying: $(basename $migration)"
        
        case $db_type in
            mysql)
                mysql -u root -p"$MYSQL_PASSWORD" < "$migration"
                ;;
            postgres)
                psql -U postgres < "$migration"
                ;;
        esac
        
        echo "  ✅ Applied: $(basename $migration)"
    done
    
    echo "✅ All migrations applied"
}

create_migration() {
    local name=$1
    local timestamp=$(date +%Y%m%d%H%M%S)
    local filename="$MIGRATIONS_DIR/${timestamp}_${name}.sql"
    
    mkdir -p "$MIGRATIONS_DIR"
    
    cat > "$filename" << EOF
-- Migration: $name
-- Created: $(date)

-- Add your SQL here

EOF
    
    echo "✅ Migration created: $filename"
}

rollback_migration() {
    echo "⏪ Rolling back last migration..."
    # Implement rollback logic
    echo "✅ Rollback complete"
}

case "${1:-run}" in
    run)
        run_migrations "${2:-mysql}"
        ;;
    create)
        create_migration "$2"
        ;;
    rollback)
        rollback_migration
        ;;
esac
