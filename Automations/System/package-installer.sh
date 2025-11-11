#!/bin/bash
# Package Installation Automation

set -e

detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
    else
        OS=$(uname -s)
    fi
}

install_packages() {
    detect_os
    
    case $OS in
        ubuntu|debian)
            apt-get update
            apt-get install -y "$@"
            ;;
        centos|rhel|fedora)
            yum install -y "$@"
            ;;
        arch)
            pacman -Sy --noconfirm "$@"
            ;;
        *)
            echo "Unsupported OS: $OS"
            exit 1
            ;;
    esac
}

install_common_packages() {
    echo "Installing common packages..."
    install_packages \
        curl \
        wget \
        git \
        vim \
        htop \
        net-tools \
        build-essential \
        python3 \
        python3-pip
}

install_docker() {
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
}

install_nodejs() {
    echo "Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
    install_packages nodejs
}

case "${1:-common}" in
    common)
        install_common_packages
        ;;
    docker)
        install_docker
        ;;
    nodejs)
        install_nodejs
        ;;
    custom)
        shift
        install_packages "$@"
        ;;
esac

echo "✅ Installation complete"
