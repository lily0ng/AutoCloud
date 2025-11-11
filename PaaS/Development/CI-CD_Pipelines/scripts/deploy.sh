#!/bin/bash

ENVIRONMENT=$1

if [ -z "$ENVIRONMENT" ]; then
    echo "Usage: $0 <environment>"
    exit 1
fi

echo "Deploying to $ENVIRONMENT environment"

# Load environment-specific variables
source "../config/$ENVIRONMENT.env"

# Initialize Terraform
cd ../terraform/$ENVIRONMENT
terraform init

# Apply Terraform changes
terraform apply -auto-approve

# Deploy application
case $ENVIRONMENT in
    "dev")
        aws elasticbeanstalk update-environment \
            --environment-name dev-environment \
            --version-label $VERSION
        ;;
    "staging")
        aws elasticbeanstalk update-environment \
            --environment-name staging-environment \
            --version-label $VERSION
        ;;
    "prod")
        # Run database backup before production deployment
        ./backup-database.sh
        
        aws elasticbeanstalk update-environment \
            --environment-name prod-environment \
            --version-label $VERSION
        ;;
    *)
        echo "Invalid environment: $ENVIRONMENT"
        exit 1
        ;;
esac

# Run post-deployment health checks
./health-check.sh $ENVIRONMENT

echo "Deployment to $ENVIRONMENT completed successfully"
