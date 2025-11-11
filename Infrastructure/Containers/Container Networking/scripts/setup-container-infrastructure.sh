#!/bin/bash

# Exit on error and undefined variables
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Log functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Check command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check system requirements
check_system_requirements() {
    log_info "Checking system requirements..."
    
    # Check if running on Linux
    if [[ "$(uname)" != "Linux" ]]; then
        log_error "This script only supports Linux systems"
        exit 1
    }

    # Check for required commands
    local required_commands=("curl" "wget" "unzip")
    for cmd in "${required_commands[@]}"; do
        if ! command_exists "$cmd"; then
            log_error "Required command '$cmd' not found. Please install it first."
            exit 1
        fi
    done
}

# Install Docker
install_docker() {
    log_info "Installing Docker..."
    if command_exists docker; then
        log_warn "Docker already installed. Skipping installation."
        return
    fi

    {
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker "$USER"
        sudo systemctl enable docker
        sudo systemctl start docker
        rm -f get-docker.sh
    } || {
        log_error "Docker installation failed"
        exit 1
    }
}

# Install Docker Compose
install_docker_compose() {
    log_info "Installing Docker Compose..."
    if command_exists docker-compose; then
        log_warn "Docker Compose already installed. Skipping installation."
        return
    }

    {
        local compose_latest
        compose_latest=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -o -E "https://.*docker-compose-$(uname -s)-$(uname -m)\"" | tr -d '"')
        sudo curl -L "$compose_latest" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    } || {
        log_error "Docker Compose installation failed"
        exit 1
    }
}

# Install AWS CLI
install_aws_cli() {
    log_info "Installing AWS CLI..."
    if command_exists aws; then
        log_warn "AWS CLI already installed. Skipping installation."
        return
    }

    {
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
        unzip -q awscliv2.zip
        sudo ./aws/install
        rm -rf aws awscliv2.zip
    } || {
        log_error "AWS CLI installation failed"
        exit 1
    }
}

# Install Azure CLI
install_azure_cli() {
    log_info "Installing Azure CLI..."
    if command_exists az; then
        log_warn "Azure CLI already installed. Skipping installation."
        return
    }

    {
        curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
    } || {
        log_error "Azure CLI installation failed"
        exit 1
    }
}

# Configure Docker daemon
configure_docker() {
    log_info "Configuring Docker daemon..."
    if [[ ! -f "docker/docker-daemon.json" ]]; then
        log_error "docker-daemon.json configuration file not found"
        exit 1
    }

    {
        sudo mkdir -p /etc/docker
        sudo cp docker/docker-daemon.json /etc/docker/daemon.json
        sudo systemctl restart docker
    } || {
        log_error "Docker daemon configuration failed"
        exit 1
    }
}

# Initialize Docker Swarm
init_docker_swarm() {
    log_info "Initializing Docker Swarm..."
    if docker node ls >/dev/null 2>&1; then
        log_warn "Docker Swarm already initialized. Skipping."
        return
    }

    {
        docker swarm init || true
    } || {
        log_error "Docker Swarm initialization failed"
        exit 1
    }
}

# Update infrastructure components
update_infrastructure() {
    log_info "Updating container infrastructure components..."

    # Update Docker if installed
    if command_exists docker; then
        log_info "Updating Docker..."
        sudo apt-get update
        sudo apt-get upgrade -y docker-ce docker-ce-cli containerd.io
    fi

    # Update Docker Compose if installed
    if command_exists docker-compose; then
        log_info "Updating Docker Compose..."
        local compose_latest
        compose_latest=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -o -E "https://.*docker-compose-$(uname -s)-$(uname -m)\"" | tr -d '"')
        sudo curl -L "$compose_latest" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi

    # Update AWS CLI if installed
    if command_exists aws; then
        log_info "Updating AWS CLI..."
        sudo aws --version
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
        unzip -q awscliv2.zip
        sudo ./aws/install --update
        rm -rf aws awscliv2.zip
    fi

    # Update Azure CLI if installed
    if command_exists az; then
        log_info "Updating Azure CLI..."
        sudo apt-get update && sudo apt-get upgrade -y azure-cli
    fi

    log_info "Container infrastructure update completed!"
}

# Show script usage
show_usage() {
    echo "Usage: $0 {install|update}"
    echo "Commands:"
    echo "  install - Install container infrastructure"
    echo "  update  - Update existing container infrastructure"
    exit 1
}

# Main installation process
main() {
    # Check if running as root
    if [[ "$EUID" -eq 0 ]]; then 
        log_error "Please do not run as root"
        exit 1
    }

    # Check system requirements
    check_system_requirements

    # Process command line arguments
    case "${1:-}" in
        "install")
            install_docker
            install_docker_compose
            install_aws_cli
            install_azure_cli
            configure_docker
            init_docker_swarm
            log_info "Container infrastructure setup completed!"
            log_info "Please log out and log back in to use Docker without sudo."
            ;;
        "update")
            update_infrastructure
            ;;
        *)
            show_usage
            ;;
    esac
}

# Trap errors
trap 'log_error "An error occurred. Exiting..." >&2' ERR

# Run main function with arguments
main "$@"
