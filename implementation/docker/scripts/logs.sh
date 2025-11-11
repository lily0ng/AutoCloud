#!/bin/bash
# View Docker logs

SERVICE=${1:-all}

if [ "$SERVICE" = "all" ]; then
    docker-compose -f docker/docker-compose.yml logs -f
else
    docker-compose -f docker/docker-compose.yml logs -f $SERVICE
fi
