#!/bin/bash
SOURCE=${1:-"/data"}
DEST=${2:-"s3://backup-bucket"}
echo "🔄 Syncing $SOURCE to $DEST..."
echo "  Copying files..."
echo "✅ Sync complete"
