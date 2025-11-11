#!/bin/bash
# SSL Certificate Check Script

DOMAINS=(
    "api.autocloud.com"
    "app.autocloud.com"
    "admin.autocloud.com"
)

WARN_DAYS=30

check_certificate() {
    local domain=$1
    
    echo "Checking certificate for: $domain"
    
    expiry_date=$(echo | openssl s_client -servername $domain -connect $domain:443 2>/dev/null | \
                  openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
    
    if [ -z "$expiry_date" ]; then
        echo "  ✗ Failed to retrieve certificate"
        return 1
    fi
    
    expiry_epoch=$(date -d "$expiry_date" +%s)
    current_epoch=$(date +%s)
    days_until_expiry=$(( ($expiry_epoch - $current_epoch) / 86400 ))
    
    echo "  Expires: $expiry_date"
    echo "  Days until expiry: $days_until_expiry"
    
    if [ $days_until_expiry -lt 0 ]; then
        echo "  ✗ EXPIRED"
        return 1
    elif [ $days_until_expiry -lt $WARN_DAYS ]; then
        echo "  ⚠ WARNING: Expires soon"
        return 2
    else
        echo "  ✓ Valid"
        return 0
    fi
}

echo "========================================="
echo "SSL Certificate Check"
echo "========================================="

for domain in "${DOMAINS[@]}"; do
    check_certificate "$domain"
    echo ""
done

echo "========================================="
echo "Check Completed"
echo "========================================="
