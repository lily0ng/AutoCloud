#!/bin/bash

# Exit on any error
set -e

echo "Starting Kubernetes cluster setup..."

# Check if minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "Installing minikube..."
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
fi

# Start minikube
echo "Starting minikube cluster..."
minikube start --driver=docker --cpus=2 --memory=4096

# Enable necessary addons
echo "Enabling addons..."
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard

# Create namespaces
echo "Creating namespaces..."
kubectl create namespace production
kubectl create namespace staging

# Apply configurations
echo "Applying Kubernetes configurations..."
kubectl apply -f ../configs/

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/app-deployment

echo "Setup complete! You can now access your cluster."
echo "To use the dashboard, run: minikube dashboard"
echo "To get service URL, run: minikube service app-service --url"
