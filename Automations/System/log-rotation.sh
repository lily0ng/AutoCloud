#!/bin/bash
# Log Rotation Automation

set -e

configure_logrotate() {
    local log_file=$1
    local config_name=$(basename "$log_file" .log)
    
    cat > "/etc/logrotate.d/$config_name" << EOF
$log_file {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root root
    sharedscripts
    postrotate
        systemctl reload rsyslog > /dev/null 2>&1 || true
    endscript
}
EOF
    
    echo "✅ Log rotation configured for $log_file"
}

rotate_now() {
    echo "Forcing log rotation..."
    logrotate -f /etc/logrotate.conf
    echo "✅ Logs rotated"
}

test_config() {
    echo "Testing logrotate configuration..."
    logrotate -d /etc/logrotate.conf
}

case "${1:-test}" in
    configure)
        configure_logrotate "$2"
        ;;
    rotate)
        rotate_now
        ;;
    test)
        test_config
        ;;
esac
