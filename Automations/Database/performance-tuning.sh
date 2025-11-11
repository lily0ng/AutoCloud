#!/bin/bash
# Database Performance Tuning

set -e

tune_mysql() {
    echo "⚡ Tuning MySQL performance..."
    
    cat >> /etc/mysql/mysql.conf.d/mysqld.cnf << EOF
# Performance tuning
innodb_buffer_pool_size = 2G
innodb_log_file_size = 512M
innodb_flush_log_at_trx_commit = 2
max_connections = 500
query_cache_size = 64M
query_cache_type = 1
EOF
    
    systemctl restart mysql
    echo "✅ MySQL tuned"
}

tune_postgresql() {
    echo "⚡ Tuning PostgreSQL performance..."
    
    cat >> /etc/postgresql/14/main/postgresql.conf << EOF
# Performance tuning
shared_buffers = 2GB
effective_cache_size = 6GB
maintenance_work_mem = 512MB
work_mem = 16MB
max_connections = 200
EOF
    
    systemctl restart postgresql
    echo "✅ PostgreSQL tuned"
}

analyze_slow_queries() {
    echo "🔍 Analyzing slow queries..."
    
    if command -v mysql &> /dev/null; then
        mysql -e "SELECT * FROM mysql.slow_log ORDER BY query_time DESC LIMIT 10;"
    fi
    
    if command -v psql &> /dev/null; then
        psql -U postgres -c "SELECT query, calls, total_time, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"
    fi
}

optimize_tables() {
    local db_name=$1
    
    echo "🔧 Optimizing tables in $db_name..."
    
    if command -v mysql &> /dev/null; then
        mysql -e "USE $db_name; OPTIMIZE TABLE $(mysql -N -e "SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema='$db_name'");"
    fi
    
    if command -v psql &> /dev/null; then
        psql -U postgres -d "$db_name" -c "VACUUM ANALYZE;"
    fi
    
    echo "✅ Tables optimized"
}

case "${1:-analyze}" in
    mysql)
        tune_mysql
        ;;
    postgres)
        tune_postgresql
        ;;
    analyze)
        analyze_slow_queries
        ;;
    optimize)
        optimize_tables "$2"
        ;;
esac
