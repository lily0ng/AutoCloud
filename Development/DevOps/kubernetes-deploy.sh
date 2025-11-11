#!/bin/bash

# Kubernetes Deployment Script

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
NAMESPACE=${NAMESPACE:-"default"}
DEPLOYMENT_NAME=${DEPLOYMENT_NAME:-"myapp"}
IMAGE=${IMAGE:-"myapp:latest"}
REPLICAS=${REPLICAS:-3}
MANIFESTS_DIR=${MANIFESTS_DIR:-"k8s"}

echo -e "${BLUE}☸️  Kubernetes Deployment${NC}"
echo "================================"

# Check kubectl
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl not found${NC}"
    exit 1
fi

# Check cluster connection
echo -e "${BLUE}🔍 Checking cluster connection...${NC}"
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}❌ Cannot connect to cluster${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Connected to cluster${NC}"
kubectl config current-context

# Create namespace if not exists
echo ""
echo -e "${BLUE}📦 Ensuring namespace exists: $NAMESPACE${NC}"
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Apply ConfigMaps
if [ -f "$MANIFESTS_DIR/configmap.yaml" ]; then
    echo -e "${BLUE}📝 Applying ConfigMaps...${NC}"
    kubectl apply -f "$MANIFESTS_DIR/configmap.yaml" -n "$NAMESPACE"
fi

# Apply Secrets
if [ -f "$MANIFESTS_DIR/secret.yaml" ]; then
    echo -e "${BLUE}🔐 Applying Secrets...${NC}"
    kubectl apply -f "$MANIFESTS_DIR/secret.yaml" -n "$NAMESPACE"
fi

# Apply PersistentVolumeClaims
if [ -f "$MANIFESTS_DIR/pvc.yaml" ]; then
    echo -e "${BLUE}💾 Applying PVCs...${NC}"
    kubectl apply -f "$MANIFESTS_DIR/pvc.yaml" -n "$NAMESPACE"
fi

# Deploy application
echo ""
echo -e "${BLUE}🚀 Deploying application...${NC}"
if [ -f "$MANIFESTS_DIR/deployment.yaml" ]; then
    kubectl apply -f "$MANIFESTS_DIR/deployment.yaml" -n "$NAMESPACE"
else
    # Create deployment from template
    cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $DEPLOYMENT_NAME
  namespace: $NAMESPACE
spec:
  replicas: $REPLICAS
  selector:
    matchLabels:
      app: $DEPLOYMENT_NAME
  template:
    metadata:
      labels:
        app: $DEPLOYMENT_NAME
    spec:
      containers:
      - name: $DEPLOYMENT_NAME
        image: $IMAGE
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
EOF
fi

# Apply Service
echo -e "${BLUE}🌐 Applying Service...${NC}"
if [ -f "$MANIFESTS_DIR/service.yaml" ]; then
    kubectl apply -f "$MANIFESTS_DIR/service.yaml" -n "$NAMESPACE"
fi

# Apply Ingress
if [ -f "$MANIFESTS_DIR/ingress.yaml" ]; then
    echo -e "${BLUE}🔀 Applying Ingress...${NC}"
    kubectl apply -f "$MANIFESTS_DIR/ingress.yaml" -n "$NAMESPACE"
fi

# Wait for rollout
echo ""
echo -e "${BLUE}⏳ Waiting for rollout to complete...${NC}"
kubectl rollout status deployment/"$DEPLOYMENT_NAME" -n "$NAMESPACE" --timeout=5m

# Get deployment status
echo ""
echo -e "${BLUE}📊 Deployment Status:${NC}"
kubectl get deployment "$DEPLOYMENT_NAME" -n "$NAMESPACE"

echo ""
echo -e "${BLUE}📦 Pods:${NC}"
kubectl get pods -l app="$DEPLOYMENT_NAME" -n "$NAMESPACE"

echo ""
echo -e "${BLUE}🌐 Services:${NC}"
kubectl get svc -n "$NAMESPACE"

# Run smoke tests
if [ "$SMOKE_TEST" = "true" ]; then
    echo ""
    echo -e "${BLUE}🧪 Running smoke tests...${NC}"
    # Add smoke test commands here
fi

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
