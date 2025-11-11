#!/bin/bash
# Network Configuration Automation

set -e

configure_static_ip() {
    local interface=$1
    local ip_address=$2
    local gateway=$3
    
    cat > "/etc/netplan/01-netcfg.yaml" << EOF
network:
  version: 2
  ethernets:
    $interface:
      addresses: [$ip_address/24]
      gateway4: $gateway
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
EOF
    
    netplan apply
    echo "✅ Static IP configured"
}

configure_dhcp() {
    local interface=$1
    
    cat > "/etc/netplan/01-netcfg.yaml" << EOF
network:
  version: 2
  ethernets:
    $interface:
      dhcp4: true
EOF
    
    netplan apply
    echo "✅ DHCP configured"
}

show_network_info() {
    echo "Network Interfaces:"
    ip addr show
    echo ""
    echo "Routing Table:"
    ip route show
}

case "${1:-show}" in
    static)
        configure_static_ip "$2" "$3" "$4"
        ;;
    dhcp)
        configure_dhcp "$2"
        ;;
    show)
        show_network_info
        ;;
esac
