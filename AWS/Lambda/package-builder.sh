#!/bin/bash
# Lambda Deployment Package Builder

set -e

FUNCTION_DIR=${1:-.}
OUTPUT_FILE=${2:-function.zip}

echo "Building Lambda deployment package..."
echo "Source: $FUNCTION_DIR"
echo "Output: $OUTPUT_FILE"

cd $FUNCTION_DIR

# Install dependencies
if [ -f "package.json" ]; then
    npm install --production
fi

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt -t .
fi

# Create zip
zip -r $OUTPUT_FILE . -x "*.git*" "*.zip" "node_modules/aws-sdk/*"

echo "Package created: $OUTPUT_FILE"
ls -lh $OUTPUT_FILE
