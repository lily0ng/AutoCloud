#!/bin/bash

# Maintenance script for logging and monitoring infrastructure
set -e

echo "Starting maintenance tasks..."

# Check service status
check_service() {
    if systemctl is-active --quiet $1; then
        echo "$1 is running"
    else
        echo "WARNING: $1 is not running"
        systemctl start $1
    fi
}

# Clean old logs
clean_logs() {
    find /var/log -type f -name "*.gz" -mtime +30 -delete
    find /var/log -type f -name "*.log.*" -mtime +30 -delete
}

# Check disk space
check_disk_space() {
    df -h | awk '{ if($5 > "80%") print "WARNING: Disk space usage above 80% on "$1 }'
}

# Rotate Prometheus data
rotate_prometheus_data() {
    promtool tsdb clean --data.retention=30d /var/lib/prometheus/data
}

# Main maintenance tasks
echo "Checking services..."
check_service node_exporter
check_service prometheus
check_service filebeat

echo "Cleaning old logs..."
clean_logs

echo "Checking disk space..."
check_disk_space

echo "Rotating Prometheus data..."
rotate_prometheus_data

echo "Maintenance completed successfully!"
