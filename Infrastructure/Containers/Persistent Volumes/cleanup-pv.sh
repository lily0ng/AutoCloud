#!/bin/bash

# Delete PVCs
echo "Deleting Persistent Volume Claims..."
kubectl delete -f pvc-config.yaml

# Wait for PVCs to be deleted
echo "Waiting for PVCs to be deleted..."
sleep 10

# Delete PVs
echo "Deleting Persistent Volumes..."
kubectl delete -f pv-config.yaml

# Delete Storage Classes
echo "Deleting Storage Classes..."
kubectl delete -f storage-class.yaml

# Optional: Remove directories (uncomment if needed)
# sudo rm -rf /mnt/data/vol1
# sudo rm -rf /mnt/data/vol2

echo "Cleanup complete!"
