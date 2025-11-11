#!/bin/bash
# Firewall Configuration Automation

set -e

configure_ufw() {
    echo "Configuring UFW firewall..."
    
    # Reset firewall
    ufw --force reset
    
    # Default policies
    ufw default deny incoming
    ufw default allow outgoing
    
    # Allow SSH
    ufw allow 22/tcp
    
    # Allow HTTP/HTTPS
    ufw allow 80/tcp
    ufw allow 443/tcp
    
    # Enable firewall
    ufw --force enable
    
    echo "✅ UFW configured"
}

configure_firewalld() {
    echo "Configuring firewalld..."
    
    systemctl start firewalld
    systemctl enable firewalld
    
    # Add services
    firewall-cmd --permanent --add-service=ssh
    firewall-cmd --permanent --add-service=http
    firewall-cmd --permanent --add-service=https
    
    # Reload
    firewall-cmd --reload
    
    echo "✅ firewalld configured"
}

add_custom_rule() {
    local port=$1
    local protocol=${2:-tcp}
    
    if command -v ufw &> /dev/null; then
        ufw allow $port/$protocol
    elif command -v firewall-cmd &> /dev/null; then
        firewall-cmd --permanent --add-port=$port/$protocol
        firewall-cmd --reload
    fi
    
    echo "✅ Rule added: $port/$protocol"
}

show_status() {
    if command -v ufw &> /dev/null; then
        ufw status verbose
    elif command -v firewall-cmd &> /dev/null; then
        firewall-cmd --list-all
    fi
}

case "${1:-configure}" in
    configure)
        if command -v ufw &> /dev/null; then
            configure_ufw
        elif command -v firewall-cmd &> /dev/null; then
            configure_firewalld
        fi
        ;;
    add-rule)
        add_custom_rule "$2" "$3"
        ;;
    status)
        show_status
        ;;
esac
