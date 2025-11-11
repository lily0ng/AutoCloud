#!/bin/bash
# VPC Network Diagram Generator

set -e

VPC_ID=${1}

if [ -z "$VPC_ID" ]; then
    echo "Usage: $0 <vpc-id>"
    exit 1
fi

echo "Generating network diagram for VPC: $VPC_ID"

# Get VPC details
echo "VPC Information:"
aws ec2 describe-vpcs --vpc-ids $VPC_ID --output table

# Get subnets
echo ""
echo "Subnets:"
aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --output table

# Get route tables
echo ""
echo "Route Tables:"
aws ec2 describe-route-tables --filters "Name=vpc-id,Values=$VPC_ID" --output table

# Get internet gateways
echo ""
echo "Internet Gateways:"
aws ec2 describe-internet-gateways --filters "Name=attachment.vpc-id,Values=$VPC_ID" --output table

# Get NAT gateways
echo ""
echo "NAT Gateways:"
aws ec2 describe-nat-gateways --filter "Name=vpc-id,Values=$VPC_ID" --output table

echo ""
echo "Network diagram generated"
