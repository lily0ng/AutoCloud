#!/bin/bash

# Docker Image Builder Script

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
IMAGE_NAME=${IMAGE_NAME:-"myapp"}
IMAGE_TAG=${IMAGE_TAG:-"latest"}
REGISTRY=${REGISTRY:-"docker.io"}
DOCKERFILE=${DOCKERFILE:-"Dockerfile"}
BUILD_CONTEXT=${BUILD_CONTEXT:-"."}
PLATFORM=${PLATFORM:-"linux/amd64"}
CACHE=${CACHE:-true}

echo -e "${BLUE}🐳 Docker Image Builder${NC}"
echo "================================"

# Validate Dockerfile exists
if [ ! -f "$DOCKERFILE" ]; then
    echo -e "${RED}❌ Dockerfile not found: $DOCKERFILE${NC}"
    exit 1
fi

# Build arguments
BUILD_ARGS=""
if [ -f ".env.build" ]; then
    echo -e "${YELLOW}📝 Loading build arguments from .env.build${NC}"
    while IFS='=' read -r key value; do
        if [[ ! $key =~ ^# ]] && [ -n "$key" ]; then
            BUILD_ARGS="$BUILD_ARGS --build-arg $key=$value"
        fi
    done < .env.build
fi

# Cache options
CACHE_OPTS=""
if [ "$CACHE" = "false" ]; then
    CACHE_OPTS="--no-cache"
fi

# Full image name
FULL_IMAGE_NAME="$REGISTRY/$IMAGE_NAME:$IMAGE_TAG"

echo -e "${BLUE}📦 Building image: $FULL_IMAGE_NAME${NC}"
echo "  Platform: $PLATFORM"
echo "  Dockerfile: $DOCKERFILE"
echo "  Context: $BUILD_CONTEXT"

# Build the image
docker build \
    --platform "$PLATFORM" \
    -t "$FULL_IMAGE_NAME" \
    -f "$DOCKERFILE" \
    $BUILD_ARGS \
    $CACHE_OPTS \
    "$BUILD_CONTEXT"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Image built successfully${NC}"
else
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi

# Tag with additional tags
if [ -n "$ADDITIONAL_TAGS" ]; then
    IFS=',' read -ra TAGS <<< "$ADDITIONAL_TAGS"
    for tag in "${TAGS[@]}"; do
        echo -e "${BLUE}🏷️  Tagging: $REGISTRY/$IMAGE_NAME:$tag${NC}"
        docker tag "$FULL_IMAGE_NAME" "$REGISTRY/$IMAGE_NAME:$tag"
    done
fi

# Image information
echo ""
echo -e "${BLUE}📊 Image Information:${NC}"
docker images "$FULL_IMAGE_NAME" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

# Security scan
if command -v trivy &> /dev/null; then
    echo ""
    echo -e "${BLUE}🔒 Running security scan...${NC}"
    trivy image "$FULL_IMAGE_NAME"
fi

# Push to registry
if [ "$PUSH" = "true" ]; then
    echo ""
    echo -e "${BLUE}📤 Pushing to registry...${NC}"
    docker push "$FULL_IMAGE_NAME"
    
    if [ -n "$ADDITIONAL_TAGS" ]; then
        IFS=',' read -ra TAGS <<< "$ADDITIONAL_TAGS"
        for tag in "${TAGS[@]}"; do
            docker push "$REGISTRY/$IMAGE_NAME:$tag"
        done
    fi
    
    echo -e "${GREEN}✅ Image pushed successfully${NC}"
fi

# Cleanup
if [ "$CLEANUP" = "true" ]; then
    echo ""
    echo -e "${YELLOW}🧹 Cleaning up dangling images...${NC}"
    docker image prune -f
fi

echo ""
echo -e "${GREEN}✅ Build complete!${NC}"
echo "Image: $FULL_IMAGE_NAME"
