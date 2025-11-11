#!/bin/sh
# Scan Docker images for vulnerabilities

set -e

IMAGES=(
    "autocloud/service-a:latest"
    "autocloud/service-b:latest"
    "autocloud/service-c:latest"
    "autocloud/web-app:latest"
    "autocloud/nginx:latest"
)

echo "========================================="
echo "Scanning Docker images for vulnerabilities"
echo "========================================="

for image in "${IMAGES[@]}"; do
    echo ""
    echo "Scanning $image..."
    trivy image --severity HIGH,CRITICAL $image
done

echo ""
echo "========================================="
echo "Security scan completed!"
echo "========================================="
