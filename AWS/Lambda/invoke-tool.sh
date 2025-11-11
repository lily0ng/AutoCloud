#!/bin/bash
# Lambda Function Invocation Tool

set -e

FUNCTION_NAME=${1}
PAYLOAD=${2:-'{}'}
INVOCATION_TYPE=${3:-RequestResponse}

if [ -z "$FUNCTION_NAME" ]; then
    echo "Usage: $0 <function-name> [payload] [invocation-type]"
    exit 1
fi

echo "Invoking Lambda function: $FUNCTION_NAME"

PAYLOAD_FILE=$(mktemp)
echo "$PAYLOAD" > $PAYLOAD_FILE

aws lambda invoke \
    --function-name $FUNCTION_NAME \
    --invocation-type $INVOCATION_TYPE \
    --payload file://$PAYLOAD_FILE \
    response.json

cat response.json
rm -f $PAYLOAD_FILE response.json
