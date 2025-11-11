#!/bin/bash

# Create necessary directories
sudo mkdir -p /mnt/data/vol1
sudo mkdir -p /mnt/data/vol2

# Set proper permissions
sudo chmod 777 /mnt/data/vol1
sudo chmod 777 /mnt/data/vol2

# Apply Storage Classes
kubectl apply -f storage-class.yaml

# Create Persistent Volumes
kubectl apply -f pv-config.yaml

# Create Persistent Volume Claims
kubectl apply -f pvc-config.yaml

# Wait for PVs to be bound
echo "Waiting for PVs to be bound..."
sleep 10

# Check status
echo "Checking Storage Classes..."
kubectl get sc

echo "Checking Persistent Volumes..."
kubectl get pv

echo "Checking Persistent Volume Claims..."
kubectl get pvc

echo "Setup complete!"
