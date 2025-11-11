#!/bin/bash
# Disk Cleanup Automation

set -e

cleanup_apt_cache() {
    echo "Cleaning APT cache..."
    apt-get clean
    apt-get autoclean
    apt-get autoremove -y
    echo "✅ APT cache cleaned"
}

cleanup_logs() {
    echo "Cleaning old logs..."
    find /var/log -name "*.log" -mtime +30 -delete
    find /var/log -name "*.gz" -mtime +30 -delete
    journalctl --vacuum-time=30d
    echo "✅ Logs cleaned"
}

cleanup_tmp() {
    echo "Cleaning temporary files..."
    find /tmp -type f -atime +7 -delete
    find /var/tmp -type f -atime +7 -delete
    echo "✅ Temporary files cleaned"
}

cleanup_docker() {
    if command -v docker &> /dev/null; then
        echo "Cleaning Docker..."
        docker system prune -af --volumes
        echo "✅ Docker cleaned"
    fi
}

show_disk_usage() {
    echo "Disk Usage:"
    df -h
    echo ""
    echo "Largest directories:"
    du -h --max-depth=1 / 2>/dev/null | sort -hr | head -10
}

case "${1:-all}" in
    apt)
        cleanup_apt_cache
        ;;
    logs)
        cleanup_logs
        ;;
    tmp)
        cleanup_tmp
        ;;
    docker)
        cleanup_docker
        ;;
    all)
        cleanup_apt_cache
        cleanup_logs
        cleanup_tmp
        cleanup_docker
        ;;
    status)
        show_disk_usage
        ;;
esac
