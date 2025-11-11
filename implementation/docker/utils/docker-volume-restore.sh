#!/bin/bash
# Restore Docker Volume

VOLUME=$1
BACKUP_FILE=$2

if [ -z "$VOLUME" ] || [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <volume_name> <backup_file>"
    exit 1
fi

echo "Restoring volume: $VOLUME from $BACKUP_FILE"
docker run --rm \
    -v $VOLUME:/target \
    -v $(dirname $BACKUP_FILE):/backup \
    alpine \
    sh -c "cd /target && tar xzf /backup/$(basename $BACKUP_FILE)"

echo "Restore completed"
