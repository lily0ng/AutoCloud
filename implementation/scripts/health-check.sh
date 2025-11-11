#!/bin/bash
# Health check script for all services

SERVICES=(
    "http://localhost:8080/health:Service-A"
    "http://localhost:8081/health:Service-B"
    "http://localhost:8082/health:Service-C"
)

echo "========================================="
echo "Health Check Report"
echo "========================================="

for service in "${SERVICES[@]}"; do
    IFS=':' read -r url name <<< "$service"
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
    
    if [ "$response" = "200" ]; then
        echo "✓ $name: HEALTHY"
    else
        echo "✗ $name: UNHEALTHY (HTTP $response)"
    fi
done

echo "========================================="
