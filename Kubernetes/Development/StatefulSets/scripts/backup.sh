#!/bin/bash

# Set environment variables
NAMESPACE="default"
APP_NAME="app-statefulset"
BACKUP_DIR="../backups"

# Create backup directory if it doesn't exist
mkdir -p ${BACKUP_DIR}

# Backup StatefulSet configuration
echo "Backing up StatefulSet configuration..."
kubectl get statefulset ${APP_NAME} -n ${NAMESPACE} -o yaml > ${BACKUP_DIR}/statefulset-backup-$(date +%Y%m%d-%H%M%S).yaml

# Backup PVC configurations
echo "Backing up PVC configurations..."
kubectl get pvc -l app=stateful-app -n ${NAMESPACE} -o yaml > ${BACKUP_DIR}/pvcs-backup-$(date +%Y%m%d-%H%M%S).yaml

echo "Backup completed successfully!"
