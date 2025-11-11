#!/bin/bash

# Monitoring Stack Setup (Prometheus + Grafana)

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

NAMESPACE=${NAMESPACE:-"monitoring"}

echo -e "${BLUE}📊 Monitoring Stack Setup${NC}"
echo "================================"

# Create namespace
echo -e "${BLUE}📦 Creating namespace...${NC}"
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Install Prometheus
echo -e "${BLUE}🔍 Installing Prometheus...${NC}"
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
    --namespace "$NAMESPACE" \
    --set prometheus.prometheusSpec.retention=30d \
    --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=50Gi \
    --set grafana.adminPassword=admin \
    --wait

echo -e "${GREEN}✅ Monitoring stack installed${NC}"

# Get access information
echo ""
echo -e "${BLUE}📝 Access Information:${NC}"
echo "Prometheus: kubectl port-forward -n $NAMESPACE svc/prometheus-kube-prometheus-prometheus 9090:9090"
echo "Grafana: kubectl port-forward -n $NAMESPACE svc/prometheus-grafana 3000:80"
echo "AlertManager: kubectl port-forward -n $NAMESPACE svc/prometheus-kube-prometheus-alertmanager 9093:9093"
echo ""
echo "Grafana credentials: admin / admin"
