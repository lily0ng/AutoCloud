#!/bin/bash
# System Performance Tuning

set -e

tune_kernel() {
    echo "Tuning kernel parameters..."
    
    cat >> /etc/sysctl.conf << EOF
# Network performance
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 67108864
net.ipv4.tcp_wmem = 4096 65536 67108864

# Connection handling
net.ipv4.tcp_max_syn_backlog = 8192
net.core.somaxconn = 1024

# File descriptors
fs.file-max = 2097152
EOF
    
    sysctl -p
    echo "✅ Kernel tuned"
}

tune_limits() {
    echo "Tuning system limits..."
    
    cat >> /etc/security/limits.conf << EOF
* soft nofile 65536
* hard nofile 65536
* soft nproc 65536
* hard nproc 65536
EOF
    
    echo "✅ Limits tuned"
}

optimize_swappiness() {
    echo "Optimizing swappiness..."
    sysctl vm.swappiness=10
    echo "vm.swappiness=10" >> /etc/sysctl.conf
    echo "✅ Swappiness optimized"
}

disable_transparent_hugepages() {
    echo "Disabling transparent hugepages..."
    echo never > /sys/kernel/mm/transparent_hugepage/enabled
    echo never > /sys/kernel/mm/transparent_hugepage/defrag
    echo "✅ Transparent hugepages disabled"
}

case "${1:-all}" in
    kernel)
        tune_kernel
        ;;
    limits)
        tune_limits
        ;;
    swap)
        optimize_swappiness
        ;;
    hugepages)
        disable_transparent_hugepages
        ;;
    all)
        tune_kernel
        tune_limits
        optimize_swappiness
        disable_transparent_hugepages
        ;;
esac
