#!/bin/bash

# Set environment variables
NAMESPACE="default"
APP_NAME="app-statefulset"

# Delete StatefulSet and related resources
echo "Cleaning up StatefulSet resources..."
kubectl delete statefulset ${APP_NAME} -n ${NAMESPACE}
kubectl delete service app-headless -n ${NAMESPACE}

# Delete PVCs
echo "Cleaning up PersistentVolumeClaims..."
kubectl delete pvc -l app=stateful-app -n ${NAMESPACE}

echo "Cleanup completed successfully!"
