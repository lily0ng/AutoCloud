#!/bin/bash
# S3 Sync Tool

set -e

SOURCE=${1}
DESTINATION=${2}
MODE=${3:-sync}

if [ -z "$SOURCE" ] || [ -z "$DESTINATION" ]; then
    echo "Usage: $0 <source> <destination> [sync|copy|move]"
    echo "Examples:"
    echo "  $0 /local/path s3://bucket/path sync"
    echo "  $0 s3://bucket1/path s3://bucket2/path copy"
    exit 1
fi

echo "========================================="
echo "S3 Sync Tool"
echo "Source: $SOURCE"
echo "Destination: $DESTINATION"
echo "Mode: $MODE"
echo "========================================="

case $MODE in
    sync)
        aws s3 sync $SOURCE $DESTINATION \
            --delete \
            --exclude ".git/*" \
            --exclude ".DS_Store"
        ;;
    copy)
        aws s3 cp $SOURCE $DESTINATION --recursive
        ;;
    move)
        aws s3 mv $SOURCE $DESTINATION --recursive
        ;;
    *)
        echo "Invalid mode: $MODE"
        exit 1
        ;;
esac

echo "Operation completed successfully!"
