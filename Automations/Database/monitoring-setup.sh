#!/bin/bash
# Database Monitoring Setup

set -e

install_prometheus_exporter() {
    local db_type=$1
    
    echo "📊 Installing Prometheus exporter for $db_type..."
    
    case $db_type in
        mysql)
            wget https://github.com/prometheus/mysqld_exporter/releases/download/v0.14.0/mysqld_exporter-0.14.0.linux-amd64.tar.gz
            tar xvf mysqld_exporter-0.14.0.linux-amd64.tar.gz
            mv mysqld_exporter-0.14.0.linux-amd64/mysqld_exporter /usr/local/bin/
            ;;
        postgres)
            wget https://github.com/prometheus-community/postgres_exporter/releases/download/v0.11.1/postgres_exporter-0.11.1.linux-amd64.tar.gz
            tar xvf postgres_exporter-0.11.1.linux-amd64.tar.gz
            mv postgres_exporter-0.11.1.linux-amd64/postgres_exporter /usr/local/bin/
            ;;
    esac
    
    echo "✅ Exporter installed"
}

setup_monitoring_dashboard() {
    echo "📈 Setting up monitoring dashboard..."
    
    # Install Grafana
    apt-get install -y grafana
    systemctl enable grafana-server
    systemctl start grafana-server
    
    echo "✅ Grafana installed on http://localhost:3000"
}

check_database_health() {
    echo "🏥 Checking database health..."
    
    if command -v mysql &> /dev/null; then
        echo "MySQL Status:"
        mysql -e "SHOW STATUS LIKE 'Threads_connected';"
        mysql -e "SHOW STATUS LIKE 'Uptime';"
    fi
    
    if command -v psql &> /dev/null; then
        echo "PostgreSQL Status:"
        psql -U postgres -c "SELECT count(*) as connections FROM pg_stat_activity;"
        psql -U postgres -c "SELECT pg_postmaster_start_time();"
    fi
}

case "${1:-health}" in
    install)
        install_prometheus_exporter "$2"
        ;;
    dashboard)
        setup_monitoring_dashboard
        ;;
    health)
        check_database_health
        ;;
esac
