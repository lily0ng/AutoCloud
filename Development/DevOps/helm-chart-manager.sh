#!/bin/bash

# Helm Chart Manager

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

CHART_NAME=${CHART_NAME:-"myapp"}
RELEASE_NAME=${RELEASE_NAME:-"myapp"}
NAMESPACE=${NAMESPACE:-"default"}
VALUES_FILE=${VALUES_FILE:-"values.yaml"}
CHART_DIR=${CHART_DIR:-"./charts/$CHART_NAME"}

echo -e "${BLUE}⎈ Helm Chart Manager${NC}"
echo "================================"

if ! command -v helm &> /dev/null; then
    echo -e "${RED}❌ Helm not found${NC}"
    exit 1
fi

function create_chart() {
    echo -e "${BLUE}📦 Creating new chart: $CHART_NAME${NC}"
    helm create "$CHART_DIR"
    echo -e "${GREEN}✅ Chart created${NC}"
}

function lint_chart() {
    echo -e "${BLUE}🔍 Linting chart...${NC}"
    helm lint "$CHART_DIR"
    echo -e "${GREEN}✅ Lint passed${NC}"
}

function package_chart() {
    echo -e "${BLUE}📦 Packaging chart...${NC}"
    helm package "$CHART_DIR" -d ./dist
    echo -e "${GREEN}✅ Chart packaged${NC}"
}

function install_chart() {
    echo -e "${BLUE}🚀 Installing chart: $RELEASE_NAME${NC}"
    
    helm upgrade --install "$RELEASE_NAME" "$CHART_DIR" \
        --namespace "$NAMESPACE" \
        --create-namespace \
        --values "$VALUES_FILE" \
        --wait \
        --timeout 5m
    
    echo -e "${GREEN}✅ Chart installed${NC}"
}

function uninstall_chart() {
    echo -e "${YELLOW}🗑️  Uninstalling chart: $RELEASE_NAME${NC}"
    helm uninstall "$RELEASE_NAME" -n "$NAMESPACE"
    echo -e "${GREEN}✅ Chart uninstalled${NC}"
}

function list_releases() {
    echo -e "${BLUE}📋 Helm Releases:${NC}"
    helm list -A
}

function get_status() {
    echo -e "${BLUE}📊 Release Status:${NC}"
    helm status "$RELEASE_NAME" -n "$NAMESPACE"
}

function rollback() {
    REVISION=${1:-0}
    echo -e "${YELLOW}⏪ Rolling back to revision: $REVISION${NC}"
    helm rollback "$RELEASE_NAME" "$REVISION" -n "$NAMESPACE"
    echo -e "${GREEN}✅ Rollback complete${NC}"
}

function show_values() {
    echo -e "${BLUE}📄 Chart Values:${NC}"
    helm show values "$CHART_DIR"
}

case "${1:-install}" in
    create)
        create_chart
        ;;
    lint)
        lint_chart
        ;;
    package)
        package_chart
        ;;
    install)
        install_chart
        ;;
    uninstall)
        uninstall_chart
        ;;
    list)
        list_releases
        ;;
    status)
        get_status
        ;;
    rollback)
        rollback "$2"
        ;;
    values)
        show_values
        ;;
    *)
        echo "Usage: $0 {create|lint|package|install|uninstall|list|status|rollback|values}"
        exit 1
        ;;
esac
