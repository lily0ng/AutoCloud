# CloudFormation Templates Collection

This repository contains a collection of AWS CloudFormation templates for deploying various cloud infrastructure components.

## Templates Overview

1. **vpc-network.yaml** - VPC networking infrastructure with public/private subnets
2. **ec2-webapp.yaml** - EC2 instance with auto-scaling and load balancer
3. **s3-backup.yaml** - S3 bucket with lifecycle policies and backup configurations
4. **lambda-api.yaml** - Serverless API using Lambda and API Gateway
5. **rds-aurora.yaml** - Aurora database cluster with read replicas

## Usage

Each template can be deployed using the AWS CloudFormation console or AWS CLI:

```bash
aws cloudformation create-stack --stack-name <stack-name> --template-body file://<template-file.yaml>
```

## Prerequisites

- AWS CLI configured with appropriate credentials
- Necessary IAM permissions to create resources
- Knowledge of AWS services and CloudFormation syntax
