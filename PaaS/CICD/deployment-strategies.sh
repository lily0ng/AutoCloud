#!/bin/bash
STRATEGY=${1:-"rolling"}
echo "🚀 Deployment strategy: $STRATEGY"
case $STRATEGY in
  rolling) echo "  Rolling update: 25% -> 50% -> 100%" ;;
  blue-green) echo "  Blue-Green: Switch traffic to new version" ;;
  canary) echo "  Canary: 5% -> 10% -> 50% -> 100%" ;;
esac
echo "✅ Strategy configured"
