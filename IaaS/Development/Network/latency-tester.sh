#!/bin/bash
TARGET=${1:-"8.8.8.8"}
echo "🏓 Testing latency to $TARGET..."
ping -c 4 "$TARGET"
echo "✅ Latency test complete"
