#!/bin/bash
# Backup Manager
BACKUP_DIR="/var/backups/compute"
mkdir -p "$BACKUP_DIR"
echo "📦 Creating backup..."
tar -czf "$BACKUP_DIR/backup-$(date +%Y%m%d).tar.gz" /data
echo "✅ Backup created"
