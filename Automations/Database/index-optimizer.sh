#!/bin/bash
# Database Index Optimizer

set -e

analyze_mysql_indexes() {
    local db_name=$1
    
    echo "🔍 Analyzing MySQL indexes for $db_name..."
    
    mysql -u root -p"$MYSQL_PASSWORD" "$db_name" << EOF
SELECT 
    table_name,
    index_name,
    cardinality,
    index_type
FROM information_schema.statistics
WHERE table_schema = '$db_name'
ORDER BY table_name, index_name;
EOF
}

find_missing_indexes() {
    local db_name=$1
    
    echo "🔍 Finding missing indexes..."
    
    mysql -u root -p"$MYSQL_PASSWORD" "$db_name" << EOF
SELECT 
    table_name,
    column_name
FROM information_schema.columns
WHERE table_schema = '$db_name'
AND column_name IN (SELECT column_name FROM information_schema.key_column_usage WHERE table_schema = '$db_name')
AND column_name NOT IN (SELECT column_name FROM information_schema.statistics WHERE table_schema = '$db_name');
EOF
}

create_index() {
    local db_name=$1
    local table=$2
    local column=$3
    local index_name="${table}_${column}_idx"
    
    echo "➕ Creating index: $index_name on $table($column)..."
    
    mysql -u root -p"$MYSQL_PASSWORD" "$db_name" -e \
        "CREATE INDEX $index_name ON $table($column);"
    
    echo "✅ Index created"
}

optimize_postgresql_indexes() {
    local db_name=$1
    
    echo "🔧 Optimizing PostgreSQL indexes..."
    
    psql -U postgres -d "$db_name" << EOF
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY schemaname, tablename;
EOF
    
    psql -U postgres -d "$db_name" -c "REINDEX DATABASE $db_name;"
    
    echo "✅ Indexes optimized"
}

case "${1:-analyze}" in
    analyze)
        analyze_mysql_indexes "$2"
        ;;
    missing)
        find_missing_indexes "$2"
        ;;
    create)
        create_index "$2" "$3" "$4"
        ;;
    optimize-postgres)
        optimize_postgresql_indexes "$2"
        ;;
esac
