#!/bin/bash

# Apply network policies
echo "Applying network policies..."
kubectl apply -f ../config/default-network-policy.yaml

# Apply service configurations
echo "Applying service configurations..."
kubectl apply -f ../config/service-config.yaml

# Apply ingress configurations
echo "Applying ingress configurations..."
kubectl apply -f ../config/ingress-config.yaml

# Verify deployments
echo "Verifying configurations..."
echo "Network Policies:"
kubectl get networkpolicies
echo "Services:"
kubectl get services
echo "Ingress:"
kubectl get ingress

# Check pods connectivity
echo "Checking pod connectivity..."
kubectl get pods -o wide

