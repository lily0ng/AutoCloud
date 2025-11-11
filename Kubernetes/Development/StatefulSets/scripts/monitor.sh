#!/bin/bash

# Set environment variables
NAMESPACE="default"
APP_NAME="app-statefulset"

# Function to display StatefulSet status
show_status() {
    echo "=== StatefulSet Status ==="
    kubectl get statefulset ${APP_NAME} -n ${NAMESPACE}
    echo -e "\n=== Pods Status ==="
    kubectl get pods -l app=stateful-app -n ${NAMESPACE}
    echo -e "\n=== PVC Status ==="
    kubectl get pvc -l app=stateful-app -n ${NAMESPACE}
}

# Continuous monitoring if argument is provided
if [ "$1" = "-w" ]; then
    while true; do
        clear
        show_status
        sleep 5
    done
else
    show_status
fi
