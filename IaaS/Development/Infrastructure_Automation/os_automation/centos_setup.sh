#!/bin/bash

# CentOS Server Setup and Hardening Script
set -e

# Update system
dnf update -y
dnf upgrade -y

# Install essential packages
dnf install -y \
    epel-release \
    curl \
    wget \
    vim \
    firewalld \
    fail2ban \
    dnf-automatic

# Configure firewall
systemctl enable firewalld
systemctl start firewalld
firewall-cmd --permanent --add-service=ssh
firewall-cmd --reload

# Configure automatic updates
sed -i 's/apply_updates = no/apply_updates = yes/' /etc/dnf/automatic.conf
systemctl enable --now dnf-automatic.timer

# Harden SSH configuration
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart sshd
