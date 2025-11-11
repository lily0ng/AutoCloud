#!/bin/bash
# System Monitoring Script

THRESHOLD_CPU=80
THRESHOLD_MEM=80
THRESHOLD_DISK=90
LOG_FILE="/var/log/system_monitor.log"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_cpu() {
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    CPU_USAGE=${CPU_USAGE%.*}
    
    if [ "$CPU_USAGE" -gt "$THRESHOLD_CPU" ]; then
        log_message "WARNING: High CPU usage: ${CPU_USAGE}%"
        return 1
    fi
    log_message "INFO: CPU usage: ${CPU_USAGE}%"
    return 0
}

check_memory() {
    MEM_USAGE=$(free | grep Mem | awk '{print ($3/$2) * 100.0}')
    MEM_USAGE=${MEM_USAGE%.*}
    
    if [ "$MEM_USAGE" -gt "$THRESHOLD_MEM" ]; then
        log_message "WARNING: High memory usage: ${MEM_USAGE}%"
        return 1
    fi
    log_message "INFO: Memory usage: ${MEM_USAGE}%"
    return 0
}

check_disk() {
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | cut -d'%' -f1)
    
    if [ "$DISK_USAGE" -gt "$THRESHOLD_DISK" ]; then
        log_message "WARNING: High disk usage: ${DISK_USAGE}%"
        return 1
    fi
    log_message "INFO: Disk usage: ${DISK_USAGE}%"
    return 0
}

check_services() {
    SERVICES=("docker" "postgresql" "redis-server")
    
    for service in "${SERVICES[@]}"; do
        if systemctl is-active --quiet "$service"; then
            log_message "INFO: Service $service is running"
        else
            log_message "ERROR: Service $service is not running"
        fi
    done
}

main() {
    log_message "=== System Monitor Check Started ==="
    
    check_cpu
    check_memory
    check_disk
    check_services
    
    log_message "=== System Monitor Check Completed ==="
}

main
