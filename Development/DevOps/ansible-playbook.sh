#!/bin/bash

# Ansible Playbook Runner

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PLAYBOOK=${PLAYBOOK:-"site.yml"}
INVENTORY=${INVENTORY:-"inventory/hosts"}
LIMIT=${LIMIT:-""}
TAGS=${TAGS:-""}
SKIP_TAGS=${SKIP_TAGS:-""}
EXTRA_VARS=${EXTRA_VARS:-""}

echo -e "${BLUE}📜 Ansible Playbook Runner${NC}"
echo "================================"

if ! command -v ansible-playbook &> /dev/null; then
    echo -e "${RED}❌ Ansible not found${NC}"
    exit 1
fi

# Build command
CMD="ansible-playbook $PLAYBOOK -i $INVENTORY"

if [ -n "$LIMIT" ]; then
    CMD="$CMD --limit $LIMIT"
fi

if [ -n "$TAGS" ]; then
    CMD="$CMD --tags $TAGS"
fi

if [ -n "$SKIP_TAGS" ]; then
    CMD="$CMD --skip-tags $SKIP_TAGS"
fi

if [ -n "$EXTRA_VARS" ]; then
    CMD="$CMD --extra-vars '$EXTRA_VARS'"
fi

if [ "$CHECK" = "true" ]; then
    CMD="$CMD --check"
fi

if [ "$DIFF" = "true" ]; then
    CMD="$CMD --diff"
fi

if [ "$VERBOSE" = "true" ]; then
    CMD="$CMD -vvv"
fi

echo -e "${BLUE}🚀 Running playbook: $PLAYBOOK${NC}"
echo "Command: $CMD"
echo ""

eval $CMD

echo ""
echo -e "${GREEN}✅ Playbook execution complete${NC}"
