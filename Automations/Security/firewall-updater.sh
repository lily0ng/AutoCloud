#!/bin/bash
# Automated Firewall Rule Updater

set -e

update_firewall_rules() {
    echo "🔥 Updating firewall rules..."
    
    # Backup current rules
    iptables-save > /etc/iptables/rules.backup
    
    # Clear existing rules
    iptables -F
    iptables -X
    
    # Default policies
    iptables -P INPUT DROP
    iptables -P FORWARD DROP
    iptables -P OUTPUT ACCEPT
    
    # Allow loopback
    iptables -A INPUT -i lo -j ACCEPT
    
    # Allow established connections
    iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    
    # Allow SSH
    iptables -A INPUT -p tcp --dport 22 -j ACCEPT
    
    # Allow HTTP/HTTPS
    iptables -A INPUT -p tcp --dport 80 -j ACCEPT
    iptables -A INPUT -p tcp --dport 443 -j ACCEPT
    
    # Save rules
    iptables-save > /etc/iptables/rules.v4
    
    echo "✅ Firewall rules updated"
}

block_ip() {
    local ip=$1
    echo "🚫 Blocking IP: $ip"
    iptables -A INPUT -s "$ip" -j DROP
    iptables-save > /etc/iptables/rules.v4
    echo "✅ IP blocked"
}

unblock_ip() {
    local ip=$1
    echo "✅ Unblocking IP: $ip"
    iptables -D INPUT -s "$ip" -j DROP
    iptables-save > /etc/iptables/rules.v4
    echo "✅ IP unblocked"
}

list_rules() {
    echo "📋 Current firewall rules:"
    iptables -L -n -v
}

block_country() {
    local country_code=$1
    echo "🌍 Blocking traffic from $country_code..."
    
    # Download country IP list
    wget -O /tmp/country-ips.txt "https://www.ipdeny.com/ipblocks/data/countries/${country_code}.zone"
    
    # Block each IP range
    while read ip; do
        iptables -A INPUT -s "$ip" -j DROP
    done < /tmp/country-ips.txt
    
    iptables-save > /etc/iptables/rules.v4
    echo "✅ Country blocked"
}

case "${1:-list}" in
    update)
        update_firewall_rules
        ;;
    block-ip)
        block_ip "$2"
        ;;
    unblock-ip)
        unblock_ip "$2"
        ;;
    block-country)
        block_country "$2"
        ;;
    list)
        list_rules
        ;;
esac
