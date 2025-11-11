#!/bin/bash
# AWS CLI Wrapper Script

set -e

AWS_REGION=${AWS_REGION:-us-east-1}
AWS_PROFILE=${AWS_PROFILE:-default}

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# List EC2 instances
list_instances() {
    log_info "Listing EC2 instances..."
    aws ec2 describe-instances \
        --region $AWS_REGION \
        --profile $AWS_PROFILE \
        --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,PublicIpAddress,Tags[?Key==`Name`].Value|[0]]' \
        --output table
}

# List S3 buckets
list_buckets() {
    log_info "Listing S3 buckets..."
    aws s3 ls --profile $AWS_PROFILE
}

# List RDS instances
list_databases() {
    log_info "Listing RDS instances..."
    aws rds describe-db-instances \
        --region $AWS_REGION \
        --profile $AWS_PROFILE \
        --query 'DBInstances[*].[DBInstanceIdentifier,DBInstanceClass,Engine,DBInstanceStatus]' \
        --output table
}

# Get cost estimate
get_costs() {
    log_info "Getting cost estimate..."
    START_DATE=$(date -d "1 month ago" +%Y-%m-%d)
    END_DATE=$(date +%Y-%m-%d)
    
    aws ce get-cost-and-usage \
        --time-period Start=$START_DATE,End=$END_DATE \
        --granularity MONTHLY \
        --metrics "UnblendedCost" \
        --profile $AWS_PROFILE \
        --output table
}

# Create snapshot
create_snapshot() {
    VOLUME_ID=$1
    if [ -z "$VOLUME_ID" ]; then
        log_error "Volume ID required"
        exit 1
    fi
    
    log_info "Creating snapshot for volume $VOLUME_ID..."
    aws ec2 create-snapshot \
        --volume-id $VOLUME_ID \
        --description "Backup-$(date +%Y%m%d)" \
        --region $AWS_REGION \
        --profile $AWS_PROFILE
}

# Main menu
case "${1:-}" in
    instances)
        list_instances
        ;;
    buckets)
        list_buckets
        ;;
    databases)
        list_databases
        ;;
    costs)
        get_costs
        ;;
    snapshot)
        create_snapshot $2
        ;;
    *)
        echo "Usage: $0 {instances|buckets|databases|costs|snapshot <volume-id>}"
        exit 1
        ;;
esac
