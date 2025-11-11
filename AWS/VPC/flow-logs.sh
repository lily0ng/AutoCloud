#!/bin/bash
# VPC Flow Logs Setup

set -e

VPC_ID=${1}
LOG_GROUP_NAME=${2:-/aws/vpc/flowlogs}

if [ -z "$VPC_ID" ]; then
    echo "Usage: $0 <vpc-id> [log-group-name]"
    exit 1
fi

echo "Setting up VPC Flow Logs for: $VPC_ID"

# Create CloudWatch log group
aws logs create-log-group --log-group-name $LOG_GROUP_NAME || true

# Create IAM role for flow logs
ROLE_NAME="vpc-flow-logs-role"
aws iam create-role --role-name $ROLE_NAME \
    --assume-role-policy-document '{
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "vpc-flow-logs.amazonaws.com"},
        "Action": "sts:AssumeRole"
      }]
    }' || true

# Attach policy
aws iam put-role-policy --role-name $ROLE_NAME \
    --policy-name vpc-flow-logs-policy \
    --policy-document '{
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
        "Resource": "*"
      }]
    }'

# Get role ARN
ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)

# Create flow log
aws ec2 create-flow-logs \
    --resource-type VPC \
    --resource-ids $VPC_ID \
    --traffic-type ALL \
    --log-destination-type cloud-watch-logs \
    --log-group-name $LOG_GROUP_NAME \
    --deliver-logs-permission-arn $ROLE_ARN

echo "VPC Flow Logs enabled successfully"
