# Cloud Monitoring Configuration

This repository contains monitoring configurations for multiple cloud providers using AWS CloudWatch as the central monitoring solution.

## Directory Structure
```
CloudWatch/
├── aws/
│   ├── cloudwatch-config.json
│   └── cloudwatch-agent.json
├── azure/
│   └── azure-metrics-config.json
├── gcp/
│   └── gcp-monitoring-config.json
└── common/
    └── alerts-config.json
```

## Setup Instructions

### AWS CloudWatch
1. Install CloudWatch agent
2. Configure IAM roles and permissions
3. Apply the configuration from `aws/cloudwatch-config.json`

### Azure Integration
1. Set up Azure Monitor export to CloudWatch
2. Configure Azure diagnostic settings
3. Apply the configuration from `azure/azure-metrics-config.json`

### GCP Integration
1. Set up GCP Cloud Monitoring export
2. Configure Pub/Sub topics for metrics export
3. Apply the configuration from `gcp/gcp-monitoring-config.json`

## Common Alerts
The `common/alerts-config.json` contains cross-cloud monitoring alerts and dashboards.
