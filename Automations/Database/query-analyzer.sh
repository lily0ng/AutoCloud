#!/bin/bash
# Database Query Analyzer

set -e

enable_slow_query_log() {
    echo "📝 Enabling slow query log..."
    
    if command -v mysql &> /dev/null; then
        mysql -e "SET GLOBAL slow_query_log = 'ON';"
        mysql -e "SET GLOBAL long_query_time = 2;"
        mysql -e "SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';"
        echo "✅ MySQL slow query log enabled"
    fi
    
    if command -v psql &> /dev/null; then
        psql -U postgres -c "ALTER SYSTEM SET log_min_duration_statement = 2000;"
        psql -U postgres -c "SELECT pg_reload_conf();"
        echo "✅ PostgreSQL slow query log enabled"
    fi
}

analyze_slow_queries() {
    echo "🔍 Analyzing slow queries..."
    
    if [ -f /var/log/mysql/slow.log ]; then
        echo "Top 10 slowest MySQL queries:"
        mysqldumpslow -s t -t 10 /var/log/mysql/slow.log
    fi
    
    if command -v psql &> /dev/null; then
        echo "Top 10 slowest PostgreSQL queries:"
        psql -U postgres -c \
            "SELECT query, calls, total_time, mean_time, max_time 
             FROM pg_stat_statements 
             ORDER BY mean_time DESC 
             LIMIT 10;"
    fi
}

explain_query() {
    local db_name=$1
    local query=$2
    
    echo "📊 Explaining query execution plan..."
    
    if command -v mysql &> /dev/null; then
        mysql -u root -p"$MYSQL_PASSWORD" "$db_name" -e "EXPLAIN $query;"
    fi
    
    if command -v psql &> /dev/null; then
        psql -U postgres -d "$db_name" -c "EXPLAIN ANALYZE $query;"
    fi
}

optimize_query() {
    echo "💡 Query optimization suggestions:"
    echo "  1. Add appropriate indexes"
    echo "  2. Avoid SELECT *"
    echo "  3. Use LIMIT for large result sets"
    echo "  4. Optimize JOIN operations"
    echo "  5. Use query caching where appropriate"
}

case "${1:-analyze}" in
    enable)
        enable_slow_query_log
        ;;
    analyze)
        analyze_slow_queries
        ;;
    explain)
        explain_query "$2" "$3"
        ;;
    optimize)
        optimize_query
        ;;
esac
