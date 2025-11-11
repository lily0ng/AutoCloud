#!/bin/bash

# Configuration
PRIMARY_IP="10.0.0.10"
SECONDARY_IP="10.0.0.11"
VIRTUAL_IP="10.0.0.100"
INTERFACE="eth0"
CHECK_INTERVAL=5
MAX_FAILURES=3

# Initialize counters
failure_count=0
is_active=false

# Function to check if primary is healthy
check_health() {
    if ping -c 1 $PRIMARY_IP >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to take over as active load balancer
become_active() {
    if [ "$is_active" = false ]; then
        ip addr add $VIRTUAL_IP/32 dev $INTERFACE
        arping -U -I $INTERFACE $VIRTUAL_IP -c 3
        systemctl restart haproxy
        is_active=true
        logger "Load Balancer Failover: Becoming active with IP $VIRTUAL_IP"
    fi
}

# Function to become passive
become_passive() {
    if [ "$is_active" = true ]; then
        ip addr del $VIRTUAL_IP/32 dev $INTERFACE
        systemctl stop haproxy
        is_active=false
        logger "Load Balancer Failover: Becoming passive"
    fi
}

# Main loop
while true; do
    if [ "$(hostname -I | grep -o $SECONDARY_IP)" ]; then
        if ! check_health; then
            ((failure_count++))
            logger "Load Balancer Failover: Primary health check failed ($failure_count/$MAX_FAILURES)"
            
            if [ $failure_count -ge $MAX_FAILURES ]; then
                become_active
            fi
        else
            failure_count=0
            become_passive
        fi
    fi
    
    sleep $CHECK_INTERVAL
done
