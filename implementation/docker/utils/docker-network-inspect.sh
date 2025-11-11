#!/bin/bash
# Inspect Docker Networks

NETWORK=${1:-autocloud-network}

echo "========================================="
echo "Network: $NETWORK"
echo "========================================="

docker network inspect $NETWORK | jq '.[0] | {Name, Driver, Scope, Containers}'

echo ""
echo "Connected Containers:"
docker network inspect $NETWORK | jq '.[0].Containers | to_entries[] | {Name: .value.Name, IPv4Address: .value.IPv4Address}'
