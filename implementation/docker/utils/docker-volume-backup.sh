#!/bin/bash
# Backup Docker Volume

VOLUME=$1
BACKUP_DIR=${2:-./volume-backups}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

if [ -z "$VOLUME" ]; then
    echo "Usage: $0 <volume_name> [backup_dir]"
    exit 1
fi

mkdir -p $BACKUP_DIR

echo "Backing up volume: $VOLUME"
docker run --rm \
    -v $VOLUME:/source:ro \
    -v $BACKUP_DIR:/backup \
    alpine \
    tar czf /backup/${VOLUME}_${TIMESTAMP}.tar.gz -C /source .

echo "Backup completed: $BACKUP_DIR/${VOLUME}_${TIMESTAMP}.tar.gz"
