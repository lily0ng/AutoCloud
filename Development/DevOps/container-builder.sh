#!/bin/bash
# Container Image Builder
IMAGE_NAME=${1:-"my-app"}
VERSION=${2:-"latest"}
REGISTRY=${REGISTRY:-"docker.io"}

echo "🐳 Building container image: $IMAGE_NAME:$VERSION"
echo "  Building..."
docker build -t "$IMAGE_NAME:$VERSION" .
echo "  Tagging..."
docker tag "$IMAGE_NAME:$VERSION" "$REGISTRY/$IMAGE_NAME:$VERSION"
echo "  Pushing to registry..."
docker push "$REGISTRY/$IMAGE_NAME:$VERSION"
echo "✅ Image built and pushed: $REGISTRY/$IMAGE_NAME:$VERSION"
