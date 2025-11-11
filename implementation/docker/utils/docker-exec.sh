#!/bin/bash
# Execute command in Docker container

CONTAINER=$1
shift
COMMAND="$@"

if [ -z "$CONTAINER" ]; then
    echo "Usage: $0 <container_name> <command>"
    exit 1
fi

docker exec -it $CONTAINER $COMMAND
