#!/bin/bash
echo "🧹 Cleaning up old data..."
find /data -mtime +30 -delete
echo "✅ Cleanup complete"
