#!/bin/bash
# Service Monitoring Script

set -e

SERVICES=(
    "nginx"
    "mysql"
    "redis"
    "docker"
)

check_service() {
    local service=$1
    
    if systemctl is-active --quiet "$service"; then
        echo "✅ $service is running"
        return 0
    else
        echo "❌ $service is not running"
        return 1
    fi
}

restart_service() {
    local service=$1
    
    echo "Restarting $service..."
    systemctl restart "$service"
    
    if systemctl is-active --quiet "$service"; then
        echo "✅ $service restarted successfully"
    else
        echo "❌ Failed to restart $service"
        exit 1
    fi
}

monitor_all() {
    echo "Monitoring services..."
    
    for service in "${SERVICES[@]}"; do
        if ! check_service "$service"; then
            echo "Attempting to restart $service..."
            restart_service "$service"
        fi
    done
}

show_status() {
    for service in "${SERVICES[@]}"; do
        systemctl status "$service" --no-pager || true
    done
}

case "${1:-monitor}" in
    check)
        check_service "$2"
        ;;
    restart)
        restart_service "$2"
        ;;
    monitor)
        monitor_all
        ;;
    status)
        show_status
        ;;
esac
