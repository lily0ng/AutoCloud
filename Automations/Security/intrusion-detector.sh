#!/bin/bash
# Intrusion Detection System

set -e

install_ids() {
    echo "🛡️  Installing intrusion detection system..."
    
    apt-get update
    apt-get install -y fail2ban aide
    
    # Configure fail2ban
    cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
EOF
    
    systemctl enable fail2ban
    systemctl start fail2ban
    
    echo "✅ IDS installed"
}

scan_for_rootkits() {
    echo "🔍 Scanning for rootkits..."
    
    if ! command -v rkhunter &> /dev/null; then
        apt-get install -y rkhunter
    fi
    
    rkhunter --update
    rkhunter --check --skip-keypress
    
    echo "✅ Rootkit scan complete"
}

check_file_integrity() {
    echo "🔍 Checking file integrity..."
    
    if [ ! -f /var/lib/aide/aide.db ]; then
        echo "Initializing AIDE database..."
        aideinit
    fi
    
    aide --check
    
    echo "✅ File integrity check complete"
}

monitor_failed_logins() {
    echo "🔍 Monitoring failed login attempts..."
    
    echo "Recent failed SSH attempts:"
    grep "Failed password" /var/log/auth.log | tail -20
    
    echo ""
    echo "Banned IPs:"
    fail2ban-client status sshd
}

analyze_logs() {
    echo "📊 Analyzing security logs..."
    
    echo "Top failed login attempts by IP:"
    grep "Failed password" /var/log/auth.log | \
        awk '{print $(NF-3)}' | \
        sort | uniq -c | sort -rn | head -10
    
    echo ""
    echo "Suspicious sudo attempts:"
    grep "sudo" /var/log/auth.log | grep "FAILED" | tail -10
}

case "${1:-monitor}" in
    install)
        install_ids
        ;;
    rootkit)
        scan_for_rootkits
        ;;
    integrity)
        check_file_integrity
        ;;
    monitor)
        monitor_failed_logins
        ;;
    analyze)
        analyze_logs
        ;;
esac
