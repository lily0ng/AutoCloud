#!/bin/bash

# Default values
NAMESPACE="default"
RELEASE_NAME="myapp"
CHART_PATH="./mychart"
VALUES_FILE="./mychart/values.yaml"

# Help function
show_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -n, --namespace    Kubernetes namespace (default: default)"
    echo "  -r, --release      Release name (default: myapp)"
    echo "  -c, --chart        Chart path (default: ./mychart)"
    echo "  -v, --values       Values file path (default: ./mychart/values.yaml)"
    echo "  -h, --help         Show this help message"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -n|--namespace)
        NAMESPACE="$2"
        shift
        shift
        ;;
        -r|--release)
        RELEASE_NAME="$2"
        shift
        shift
        ;;
        -c|--chart)
        CHART_PATH="$2"
        shift
        shift
        ;;
        -v|--values)
        VALUES_FILE="$2"
        shift
        shift
        ;;
        -h|--help)
        show_help
        exit 0
        ;;
        *)
        echo "Unknown option: $1"
        show_help
        exit 1
        ;;
    esac
done

# Check if helm is installed
if ! command -v helm &> /dev/null; then
    echo "Error: helm is not installed"
    exit 1
fi

# Create namespace if it doesn't exist
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Deploy/upgrade the helm chart
echo "Deploying chart to namespace: $NAMESPACE"
helm upgrade --install $RELEASE_NAME $CHART_PATH \
    --namespace $NAMESPACE \
    --values $VALUES_FILE \
    --wait \
    --timeout 5m

if [ $? -eq 0 ]; then
    echo "Deployment successful!"
    echo "To check the deployment status, run:"
    echo "kubectl get all -n $NAMESPACE"
else
    echo "Deployment failed!"
    exit 1
fi
