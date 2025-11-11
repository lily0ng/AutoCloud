#!/bin/bash

# Exit on error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Default values
CLOUD_PROVIDER=""
REGION=""
RESOURCE_GROUP=""

usage() {
    echo "Usage: $0 [-p cloud_provider] [-r region] [-g resource_group]"
    echo "  -p: Cloud provider (aws/azure)"
    echo "  -r: Region (e.g., us-east-1 for AWS, eastus for Azure)"
    echo "  -g: Resource group name (Azure only)"
    exit 1
}

deploy_to_aws() {
    echo "Deploying to AWS ECS..."
    
    # Create ECS cluster
    aws ecs create-cluster --cluster-name container-cluster
    
    # Register task definition
    aws ecs register-task-definition --cli-input-json file://aws/ecs-task-definition.json
    
    # Create service
    aws ecs create-service \
        --cluster container-cluster \
        --service-name container-service \
        --task-definition container-app \
        --desired-count 2 \
        --launch-type FARGATE \
        --network-configuration "awsvpcConfiguration={subnets=[subnet-12345678],securityGroups=[sg-12345678],assignPublicIp=ENABLED}"
}

deploy_to_azure() {
    echo "Deploying to Azure Container Instances..."
    
    # Create resource group if it doesn't exist
    az group create --name $RESOURCE_GROUP --location $REGION
    
    # Deploy container group
    az container create \
        --resource-group $RESOURCE_GROUP \
        --file azure/container-instance.yaml
}

# Parse command line arguments
while getopts "p:r:g:" opt; do
    case $opt in
        p) CLOUD_PROVIDER=$OPTARG ;;
        r) REGION=$OPTARG ;;
        g) RESOURCE_GROUP=$OPTARG ;;
        ?) usage ;;
    esac
done

# Validate inputs
if [ -z "$CLOUD_PROVIDER" ] || [ -z "$REGION" ]; then
    echo -e "${RED}Error: Cloud provider and region are required${NC}"
    usage
fi

if [ "$CLOUD_PROVIDER" = "azure" ] && [ -z "$RESOURCE_GROUP" ]; then
    echo -e "${RED}Error: Resource group is required for Azure deployment${NC}"
    usage
fi

# Deploy based on cloud provider
case $CLOUD_PROVIDER in
    "aws")
        deploy_to_aws
        ;;
    "azure")
        deploy_to_azure
        ;;
    *)
        echo -e "${RED}Error: Invalid cloud provider. Use 'aws' or 'azure'${NC}"
        usage
        ;;
esac

echo -e "${GREEN}Deployment completed successfully!${NC}"
