#!/bin/bash
# Patch Management Automation

set -e

update_system() {
    echo "Updating system packages..."
    
    if command -v apt-get &> /dev/null; then
        apt-get update
        apt-get upgrade -y
        apt-get dist-upgrade -y
    elif command -v yum &> /dev/null; then
        yum update -y
    fi
    
    echo "✅ System updated"
}

security_updates_only() {
    echo "Installing security updates..."
    
    if command -v unattended-upgrade &> /dev/null; then
        unattended-upgrade
    else
        apt-get install -y unattended-upgrades
        dpkg-reconfigure -plow unattended-upgrades
    fi
    
    echo "✅ Security updates installed"
}

check_updates() {
    echo "Checking for available updates..."
    
    if command -v apt-get &> /dev/null; then
        apt-get update
        apt list --upgradable
    elif command -v yum &> /dev/null; then
        yum check-update
    fi
}

auto_update_config() {
    echo "Configuring automatic updates..."
    
    cat > /etc/apt/apt.conf.d/50unattended-upgrades << EOF
Unattended-Upgrade::Allowed-Origins {
    "\${distro_id}:\${distro_codename}-security";
};
Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::MinimalSteps "true";
Unattended-Upgrade::Automatic-Reboot "false";
EOF
    
    echo "✅ Auto-update configured"
}

case "${1:-update}" in
    update)
        update_system
        ;;
    security)
        security_updates_only
        ;;
    check)
        check_updates
        ;;
    auto-config)
        auto_update_config
        ;;
esac
