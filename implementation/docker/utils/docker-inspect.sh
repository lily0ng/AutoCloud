#!/bin/bash
# Inspect Docker Container

CONTAINER=$1

if [ -z "$CONTAINER" ]; then
    echo "Usage: $0 <container_name>"
    exit 1
fi

echo "========================================="
echo "Container: $CONTAINER"
echo "========================================="

echo ""
echo "Basic Info:"
docker inspect $CONTAINER | jq '.[0] | {Name, State, Created, RestartCount}'

echo ""
echo "Network Settings:"
docker inspect $CONTAINER | jq '.[0].NetworkSettings.Networks'

echo ""
echo "Mounts:"
docker inspect $CONTAINER | jq '.[0].Mounts'

echo ""
echo "Environment Variables:"
docker inspect $CONTAINER | jq '.[0].Config.Env'
