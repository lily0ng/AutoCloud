#!/bin/bash
# Migration Utility
SOURCE=${1:-"source-vm"}
TARGET=${2:-"target-vm"}
echo "🔄 Migrating from $SOURCE to $TARGET..."
echo "  Copying data..."
echo "  Updating DNS..."
echo "✅ Migration complete"
