#!/bin/bash
# Database Connection Pool Configuration

set -e

configure_pgbouncer() {
    echo "🔧 Configuring PgBouncer..."
    
    apt-get install -y pgbouncer
    
    cat > /etc/pgbouncer/pgbouncer.ini << EOF
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
listen_addr = *
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 3
max_db_connections = 100
EOF
    
    systemctl enable pgbouncer
    systemctl start pgbouncer
    
    echo "✅ PgBouncer configured on port 6432"
}

configure_mysql_pool() {
    echo "🔧 Configuring MySQL connection pool..."
    
    cat >> /etc/mysql/mysql.conf.d/mysqld.cnf << EOF
# Connection pool settings
max_connections = 500
thread_cache_size = 50
table_open_cache = 4000
EOF
    
    systemctl restart mysql
    
    echo "✅ MySQL connection pool configured"
}

monitor_connections() {
    echo "📊 Monitoring database connections..."
    
    if command -v mysql &> /dev/null; then
        echo "MySQL Connections:"
        mysql -e "SHOW STATUS LIKE 'Threads_connected';"
        mysql -e "SHOW STATUS LIKE 'Max_used_connections';"
    fi
    
    if command -v psql &> /dev/null; then
        echo "PostgreSQL Connections:"
        psql -U postgres -c "SELECT count(*) as total_connections FROM pg_stat_activity;"
        psql -U postgres -c "SELECT state, count(*) FROM pg_stat_activity GROUP BY state;"
    fi
}

case "${1:-monitor}" in
    pgbouncer)
        configure_pgbouncer
        ;;
    mysql)
        configure_mysql_pool
        ;;
    monitor)
        monitor_connections
        ;;
esac
