#!/bin/bash
# Incident Response Automation
set -e

isolate_system() {
    echo "🚨 Isolating compromised system..."
    iptables -P INPUT DROP
    iptables -P OUTPUT DROP
    iptables -P FORWARD DROP
    echo "✅ System isolated"
}

collect_evidence() {
    local evidence_dir="/var/evidence/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$evidence_dir"
    
    echo "📦 Collecting evidence..."
    cp /var/log/auth.log "$evidence_dir/"
    cp /var/log/syslog "$evidence_dir/"
    netstat -an > "$evidence_dir/network.txt"
    ps aux > "$evidence_dir/processes.txt"
    
    echo "✅ Evidence collected: $evidence_dir"
}

case "${1:-collect}" in
    isolate) isolate_system ;;
    collect) collect_evidence ;;
esac
