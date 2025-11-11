#!/bin/bash
# Security Patch Deployer
set -e

deploy_security_patches() {
    echo "🔒 Deploying security patches..."
    apt-get update
    apt-get upgrade -y --security-only
    echo "✅ Security patches deployed"
}

check_patches() {
    echo "📋 Checking available security patches..."
    apt-get update
    apt list --upgradable | grep -i security
}

case "${1:-deploy}" in
    deploy) deploy_security_patches ;;
    check) check_patches ;;
esac
