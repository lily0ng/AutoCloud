#!/bin/bash
# AutoCloud - Server Provisioning Script
# Automated server setup and configuration

set -e

# Configuration
SERVER_NAME=${1:-autocloud-server}
ENVIRONMENT=${2:-production}
REGION=${3:-us-east-1}

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "========================================="
echo "AutoCloud Server Provisioning"
echo "========================================="
echo "Server: $SERVER_NAME"
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"
echo ""

# Update system packages
log_info "Updating system packages..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update -y
    sudo apt-get upgrade -y
elif command -v yum &> /dev/null; then
    sudo yum update -y
fi

# Install essential packages
log_info "Installing essential packages..."
PACKAGES=(
    "curl"
    "wget"
    "git"
    "vim"
    "htop"
    "net-tools"
    "build-essential"
    "python3"
    "python3-pip"
)

for package in "${PACKAGES[@]}"; do
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y $package
    elif command -v yum &> /dev/null; then
        sudo yum install -y $package
    fi
done

# Install Docker
log_info "Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    log_info "Docker installed successfully"
else
    log_warn "Docker already installed"
fi

# Install Docker Compose
log_info "Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    log_info "Docker Compose installed successfully"
else
    log_warn "Docker Compose already installed"
fi

# Install Kubernetes tools
log_info "Installing Kubernetes tools..."
if ! command -v kubectl &> /dev/null; then
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    rm kubectl
    log_info "kubectl installed successfully"
else
    log_warn "kubectl already installed"
fi

# Install AWS CLI
log_info "Installing AWS CLI..."
if ! command -v aws &> /dev/null; then
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    rm -rf aws awscliv2.zip
    log_info "AWS CLI installed successfully"
else
    log_warn "AWS CLI already installed"
fi

# Install Terraform
log_info "Installing Terraform..."
if ! command -v terraform &> /dev/null; then
    wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
    sudo apt-get update && sudo apt-get install -y terraform
    log_info "Terraform installed successfully"
else
    log_warn "Terraform already installed"
fi

# Configure firewall
log_info "Configuring firewall..."
if command -v ufw &> /dev/null; then
    sudo ufw --force enable
    sudo ufw allow 22/tcp
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw allow 8080/tcp
    log_info "Firewall configured"
fi

# Setup monitoring
log_info "Setting up monitoring..."
sudo mkdir -p /var/log/autocloud
sudo chmod 755 /var/log/autocloud

# Create system user
log_info "Creating AutoCloud system user..."
if ! id "autocloud" &>/dev/null; then
    sudo useradd -r -s /bin/bash -d /opt/autocloud -m autocloud
    log_info "User 'autocloud' created"
else
    log_warn "User 'autocloud' already exists"
fi

# Setup directories
log_info "Setting up directories..."
sudo mkdir -p /opt/autocloud/{apps,config,logs,backups}
sudo chown -R autocloud:autocloud /opt/autocloud

# Configure SSH
log_info "Configuring SSH..."
sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# Setup cron jobs
log_info "Setting up cron jobs..."
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/autocloud/scripts/backup.sh") | crontab -
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/autocloud/scripts/health-check.sh") | crontab -

# Install Node.js
log_info "Installing Node.js..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
    log_info "Node.js installed successfully"
else
    log_warn "Node.js already installed"
fi

# Install Go
log_info "Installing Go..."
if ! command -v go &> /dev/null; then
    wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
    sudo rm -rf /usr/local/go
    sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
    rm go1.21.0.linux-amd64.tar.gz
    log_info "Go installed successfully"
else
    log_warn "Go already installed"
fi

# System optimization
log_info "Optimizing system..."
echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_fin_timeout=30" | sudo tee -a /etc/sysctl.conf
echo "net.core.somaxconn=1024" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Create provisioning report
log_info "Creating provisioning report..."
cat > /tmp/provisioning-report.txt << EOF
AutoCloud Server Provisioning Report
=====================================
Server Name: $SERVER_NAME
Environment: $ENVIRONMENT
Region: $REGION
Date: $(date)

Installed Components:
- Docker: $(docker --version 2>/dev/null || echo "Not installed")
- Docker Compose: $(docker-compose --version 2>/dev/null || echo "Not installed")
- kubectl: $(kubectl version --client --short 2>/dev/null || echo "Not installed")
- AWS CLI: $(aws --version 2>/dev/null || echo "Not installed")
- Terraform: $(terraform version 2>/dev/null || echo "Not installed")
- Node.js: $(node --version 2>/dev/null || echo "Not installed")
- Go: $(go version 2>/dev/null || echo "Not installed")

System Information:
- OS: $(lsb_release -d | cut -f2)
- Kernel: $(uname -r)
- CPU: $(nproc) cores
- Memory: $(free -h | awk '/^Mem:/ {print $2}')
- Disk: $(df -h / | awk 'NR==2 {print $2}')

Status: Provisioning Completed Successfully
EOF

cat /tmp/provisioning-report.txt

echo ""
echo "========================================="
echo "Server provisioning completed!"
echo "Report saved to: /tmp/provisioning-report.txt"
echo "========================================="
echo ""
log_info "Please log out and log back in for group changes to take effect"
