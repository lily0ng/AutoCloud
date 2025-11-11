#!/bin/bash
# Database Replication Setup

set -e

setup_mysql_replication() {
    local master_host=$1
    local slave_host=$2
    
    echo "🔄 Setting up MySQL replication"
    echo "   Master: $master_host"
    echo "   Slave: $slave_host"
    
    # Configure master
    cat >> /etc/mysql/mysql.conf.d/mysqld.cnf << EOF
server-id = 1
log_bin = /var/log/mysql/mysql-bin.log
binlog_do_db = mydb
EOF
    
    systemctl restart mysql
    
    # Create replication user
    mysql -e "CREATE USER 'repl'@'%' IDENTIFIED BY 'password';"
    mysql -e "GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';"
    mysql -e "FLUSH PRIVILEGES;"
    
    echo "✅ MySQL replication configured"
}

setup_postgres_replication() {
    local primary_host=$1
    local standby_host=$2
    
    echo "🔄 Setting up PostgreSQL replication"
    echo "   Primary: $primary_host"
    echo "   Standby: $standby_host"
    
    # Configure primary
    cat >> /etc/postgresql/14/main/postgresql.conf << EOF
wal_level = replica
max_wal_senders = 3
wal_keep_size = 64
EOF
    
    # Configure pg_hba.conf
    echo "host replication all $standby_host/32 md5" >> /etc/postgresql/14/main/pg_hba.conf
    
    systemctl restart postgresql
    
    echo "✅ PostgreSQL replication configured"
}

check_replication_status() {
    echo "📊 Checking replication status..."
    
    if command -v mysql &> /dev/null; then
        mysql -e "SHOW SLAVE STATUS\G"
    fi
    
    if command -v psql &> /dev/null; then
        psql -U postgres -c "SELECT * FROM pg_stat_replication;"
    fi
}

case "${1:-status}" in
    mysql)
        setup_mysql_replication "$2" "$3"
        ;;
    postgres)
        setup_postgres_replication "$2" "$3"
        ;;
    status)
        check_replication_status
        ;;
esac
