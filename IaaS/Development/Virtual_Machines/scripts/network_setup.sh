#!/bin/bash

# Network Setup Script
set -e

# Load network configuration
CONFIG_DIR="../config"
NETWORK_CONFIG="$CONFIG_DIR/network_config.yaml"

# Check if configuration file exists
if [ ! -f "$NETWORK_CONFIG" ]; then
    echo "Error: Network configuration file not found!"
    exit 1
fi

# Function to setup VLAN
setup_vlan() {
    local vlan_id=$1
    local subnet=$2
    local description=$3
    
    echo "Setting up VLAN: $description (ID: $vlan_id)"
    
    # Create VLAN interface
    ip link add link eth0 name "vlan$vlan_id" type vlan id $vlan_id
    ip addr add "$subnet" dev "vlan$vlan_id"
    ip link set dev "vlan$vlan_id" up
    
    echo "VLAN $vlan_id setup completed"
}

# Function to configure security groups
setup_security_group() {
    local group=$1
    local port=$2
    local source=$3
    
    echo "Configuring security group: $group"
    
    # Add iptables rules
    iptables -A INPUT -p tcp --dport $port -s $source -j ACCEPT
    
    echo "Security group rule added for $group"
}

# Function to setup load balancer
setup_load_balancer() {
    echo "Setting up load balancer..."
    
    # Install HAProxy if not present
    if ! command -v haproxy &> /dev/null; then
        apt-get update
        apt-get install -y haproxy
    fi
    
    # Basic HAProxy configuration
    cat > /etc/haproxy/haproxy.cfg << EOF
global
    log /dev/log local0
    maxconn 4096
    user haproxy
    group haproxy
    daemon

defaults
    log global
    mode http
    option httplog
    option dontlognull
    timeout connect 5000
    timeout client 50000
    timeout server 50000

frontend http_front
    bind *:80
    default_backend http_back

backend http_back
    balance roundrobin
    server web1 192.168.10.10:80 check
    server web2 192.168.10.11:80 check
EOF
    
    # Restart HAProxy
    systemctl restart haproxy
    
    echo "Load balancer setup completed"
}

# Main setup process
echo "Starting network setup process..."

# Setup VLANs
setup_vlan 10 "192.168.10.0/24" "Web Server Network"
setup_vlan 20 "192.168.20.0/24" "Database Server Network"
setup_vlan 30 "192.168.30.0/24" "Cache Server Network"

# Configure security groups
setup_security_group "web" 80 "0.0.0.0/0"
setup_security_group "web" 443 "0.0.0.0/0"
setup_security_group "database" 3306 "192.168.10.0/24"
setup_security_group "cache" 6379 "192.168.10.0/24"

# Setup load balancer
setup_load_balancer

echo "Network setup completed successfully!"
