#!/bin/bash
# IAM Permission Boundary Manager

set -e

USER_NAME=${1}
BOUNDARY_POLICY_ARN=${2}

if [ -z "$USER_NAME" ] || [ -z "$BOUNDARY_POLICY_ARN" ]; then
    echo "Usage: $0 <user-name> <boundary-policy-arn>"
    exit 1
fi

echo "Setting permission boundary for user: $USER_NAME"

aws iam put-user-permissions-boundary \
    --user-name $USER_NAME \
    --permissions-boundary $BOUNDARY_POLICY_ARN

echo "Permission boundary set successfully"
