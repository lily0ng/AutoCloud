#!/bin/bash
# RDS Performance Insights Monitor

set -e

DB_INSTANCE_ID=${1:-autocloud-db}
METRIC_PERIOD=${2:-300}

echo "========================================="
echo "RDS Performance Insights"
echo "DB Instance: $DB_INSTANCE_ID"
echo "========================================="

# Enable Performance Insights
echo "Enabling Performance Insights..."
aws rds modify-db-instance \
    --db-instance-identifier $DB_INSTANCE_ID \
    --enable-performance-insights \
    --performance-insights-retention-period 7 \
    --apply-immediately

# Get Performance Insights metrics
echo ""
echo "Fetching performance metrics..."

# CPU Utilization
echo "CPU Utilization:"
aws cloudwatch get-metric-statistics \
    --namespace AWS/RDS \
    --metric-name CPUUtilization \
    --dimensions Name=DBInstanceIdentifier,Value=$DB_INSTANCE_ID \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period $METRIC_PERIOD \
    --statistics Average \
    --query 'Datapoints[*].[Timestamp,Average]' \
    --output table

# Database Connections
echo ""
echo "Database Connections:"
aws cloudwatch get-metric-statistics \
    --namespace AWS/RDS \
    --metric-name DatabaseConnections \
    --dimensions Name=DBInstanceIdentifier,Value=$DB_INSTANCE_ID \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period $METRIC_PERIOD \
    --statistics Average \
    --query 'Datapoints[*].[Timestamp,Average]' \
    --output table

# Read/Write IOPS
echo ""
echo "Read IOPS:"
aws cloudwatch get-metric-statistics \
    --namespace AWS/RDS \
    --metric-name ReadIOPS \
    --dimensions Name=DBInstanceIdentifier,Value=$DB_INSTANCE_ID \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period $METRIC_PERIOD \
    --statistics Average \
    --query 'Datapoints[*].[Timestamp,Average]' \
    --output table

echo ""
echo "========================================="
echo "Performance insights retrieved!"
echo "========================================="
