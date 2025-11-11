#!/bin/bash
# Security Scanning Script
set -e

echo "🔒 Running security scans..."

# Dependency scanning
if command -v npm &> /dev/null; then
    npm audit
fi

# Container scanning
if command -v trivy &> /dev/null; then
    trivy image myapp:latest
fi

# SAST scanning
if command -v semgrep &> /dev/null; then
    semgrep --config=auto .
fi

echo "✅ Security scan complete"
