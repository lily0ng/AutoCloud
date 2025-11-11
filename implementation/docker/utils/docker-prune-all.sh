#!/bin/bash
# Prune all Docker resources

echo "========================================="
echo "Docker System Prune"
echo "========================================="

echo "Current disk usage:"
docker system df

echo ""
read -p "This will remove all unused containers, networks, images, and volumes. Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Cancelled"
    exit 0
fi

echo ""
echo "Pruning system..."
docker system prune -a --volumes -f

echo ""
echo "New disk usage:"
docker system df

echo ""
echo "========================================="
echo "Prune completed!"
echo "========================================="
