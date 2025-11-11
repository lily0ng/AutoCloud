#!/bin/bash

# Logging Stack Setup (EFK - Elasticsearch, Fluentd, Kibana)

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

NAMESPACE=${NAMESPACE:-"logging"}

echo -e "${BLUE}📝 Logging Stack Setup${NC}"
echo "================================"

# Create namespace
echo -e "${BLUE}📦 Creating namespace...${NC}"
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Install Elasticsearch
echo -e "${BLUE}🔍 Installing Elasticsearch...${NC}"
helm repo add elastic https://helm.elastic.co
helm repo update

helm upgrade --install elasticsearch elastic/elasticsearch \
    --namespace "$NAMESPACE" \
    --set replicas=3 \
    --set volumeClaimTemplate.resources.requests.storage=30Gi \
    --wait

# Install Kibana
echo -e "${BLUE}📊 Installing Kibana...${NC}"
helm upgrade --install kibana elastic/kibana \
    --namespace "$NAMESPACE" \
    --wait

# Install Fluentd
echo -e "${BLUE}📤 Installing Fluentd...${NC}"
helm repo add fluent https://fluent.github.io/helm-charts
helm upgrade --install fluentd fluent/fluentd \
    --namespace "$NAMESPACE" \
    --wait

echo -e "${GREEN}✅ Logging stack installed${NC}"

echo ""
echo -e "${BLUE}📝 Access Information:${NC}"
echo "Kibana: kubectl port-forward -n $NAMESPACE svc/kibana-kibana 5601:5601"
