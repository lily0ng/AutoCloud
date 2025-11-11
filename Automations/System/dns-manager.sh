#!/bin/bash
# DNS Configuration Manager

set -e

configure_dns() {
    local dns1=${1:-8.8.8.8}
    local dns2=${2:-8.8.4.4}
    
    cat > /etc/resolv.conf << EOF
nameserver $dns1
nameserver $dns2
EOF
    
    echo "✅ DNS configured: $dns1, $dns2"
}

add_hosts_entry() {
    local ip=$1
    local hostname=$2
    
    echo "$ip $hostname" >> /etc/hosts
    echo "✅ Host entry added: $ip $hostname"
}

show_dns_config() {
    echo "DNS Configuration:"
    cat /etc/resolv.conf
    echo ""
    echo "Hosts file:"
    cat /etc/hosts
}

test_dns() {
    local domain=${1:-google.com}
    echo "Testing DNS resolution for $domain..."
    nslookup "$domain"
}

case "${1:-show}" in
    configure)
        configure_dns "$2" "$3"
        ;;
    add-host)
        add_hosts_entry "$2" "$3"
        ;;
    show)
        show_dns_config
        ;;
    test)
        test_dns "$2"
        ;;
esac
