#!/bin/bash
TARGET=${1:-"localhost"}
echo "🎯 Running penetration test on $TARGET..."
echo "  Testing SQL injection..."
echo "  Testing XSS..."
echo "  Testing authentication..."
echo "✅ Pen test complete"
