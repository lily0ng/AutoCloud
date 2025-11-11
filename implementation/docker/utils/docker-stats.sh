#!/bin/bash
# Docker Container Statistics

echo "========================================="
echo "Docker Container Statistics"
echo "========================================="

docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"

echo ""
echo "Disk Usage:"
docker system df

echo ""
echo "Volume Usage:"
docker volume ls -q | xargs docker volume inspect | grep -A 5 Mountpoint
