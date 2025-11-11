#!/bin/bash
# Security Hardening Script

set -e

disable_root_login() {
    echo "Disabling root SSH login..."
    sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
    systemctl restart sshd
    echo "✅ Root login disabled"
}

configure_ssh() {
    echo "Hardening SSH configuration..."
    
    cat >> /etc/ssh/sshd_config << EOF
Protocol 2
PermitEmptyPasswords no
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
EOF
    
    systemctl restart sshd
    echo "✅ SSH hardened"
}

install_fail2ban() {
    echo "Installing fail2ban..."
    apt-get install -y fail2ban
    
    cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
EOF
    
    systemctl enable fail2ban
    systemctl start fail2ban
    echo "✅ fail2ban installed"
}

configure_firewall() {
    echo "Configuring firewall..."
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow ssh
    ufw --force enable
    echo "✅ Firewall configured"
}

disable_unused_services() {
    echo "Disabling unused services..."
    systemctl disable avahi-daemon || true
    systemctl disable cups || true
    echo "✅ Unused services disabled"
}

case "${1:-all}" in
    ssh)
        disable_root_login
        configure_ssh
        ;;
    fail2ban)
        install_fail2ban
        ;;
    firewall)
        configure_firewall
        ;;
    services)
        disable_unused_services
        ;;
    all)
        disable_root_login
        configure_ssh
        install_fail2ban
        configure_firewall
        disable_unused_services
        ;;
esac
