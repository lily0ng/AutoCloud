#!/bin/bash

# Build Optimization Script for Frontend Applications

set -e

echo "🚀 Starting build optimization..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BUILD_DIR="dist"
ANALYZE=${ANALYZE:-false}

# Clean previous build
echo "🧹 Cleaning previous build..."
rm -rf $BUILD_DIR
rm -rf node_modules/.cache

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm ci --prefer-offline
fi

# Run linting
echo "🔍 Running linter..."
npm run lint || {
    echo -e "${YELLOW}⚠️  Linting warnings found${NC}"
}

# Run type checking
echo "📝 Running type check..."
npm run type-check || {
    echo -e "${RED}❌ Type checking failed${NC}"
    exit 1
}

# Run tests
echo "🧪 Running tests..."
npm run test -- --passWithNoTests || {
    echo -e "${RED}❌ Tests failed${NC}"
    exit 1
}

# Build the application
echo "🏗️  Building application..."
if [ "$ANALYZE" = "true" ]; then
    ANALYZE=true npm run build
else
    npm run build
fi

# Optimize images
if command -v imagemin &> /dev/null; then
    echo "🖼️  Optimizing images..."
    imagemin $BUILD_DIR/assets/images/* --out-dir=$BUILD_DIR/assets/images
fi

# Generate gzip files
echo "📦 Generating gzip files..."
find $BUILD_DIR -type f \( -name '*.js' -o -name '*.css' -o -name '*.html' \) -exec gzip -k {} \;

# Generate brotli files if available
if command -v brotli &> /dev/null; then
    echo "📦 Generating brotli files..."
    find $BUILD_DIR -type f \( -name '*.js' -o -name '*.css' -o -name '*.html' \) -exec brotli {} -o {}.br \;
fi

# Calculate bundle sizes
echo "📊 Bundle sizes:"
du -sh $BUILD_DIR
du -sh $BUILD_DIR/assets/js/*.js 2>/dev/null || true
du -sh $BUILD_DIR/assets/css/*.css 2>/dev/null || true

# Check bundle size limits
MAX_JS_SIZE=500 # KB
for file in $BUILD_DIR/assets/js/*.js; do
    if [ -f "$file" ]; then
        size=$(du -k "$file" | cut -f1)
        if [ $size -gt $MAX_JS_SIZE ]; then
            echo -e "${YELLOW}⚠️  Warning: $file is larger than ${MAX_JS_SIZE}KB${NC}"
        fi
    fi
done

# Generate build report
echo "📄 Generating build report..."
cat > $BUILD_DIR/build-report.txt << EOF
Build Report
============
Build Date: $(date)
Build Directory: $BUILD_DIR
Total Size: $(du -sh $BUILD_DIR | cut -f1)

JavaScript Files:
$(find $BUILD_DIR -name '*.js' -exec du -h {} \; | sort -h)

CSS Files:
$(find $BUILD_DIR -name '*.css' -exec du -h {} \; | sort -h)

HTML Files:
$(find $BUILD_DIR -name '*.html' -exec du -h {} \; | sort -h)
EOF

echo -e "${GREEN}✅ Build optimization complete!${NC}"
echo "📁 Build output: $BUILD_DIR"
echo "📄 Build report: $BUILD_DIR/build-report.txt"

# Optional: Deploy to CDN or hosting
if [ "$DEPLOY" = "true" ]; then
    echo "🚀 Deploying to production..."
    # Add deployment commands here
fi
