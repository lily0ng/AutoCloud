# AWS CloudFormation Infrastructure Setup

![AWS CloudFormation](https://d1.awsstatic.com/Products/product-name/diagrams/product-page-diagram-CloudFormation.ad3a4c93b4fdd3366da3da0de4a978628d2800e4.png)

## Overview
This repository contains various AWS CloudFormation templates for infrastructure provisioning. The templates are organized by different use cases and configurations.

## Directory Structure
```
.
├── README.md
├── configs/
│   ├── network/
│   ├── compute/
│   ├── storage/
│   ├── security/
│   ├── database/
│   └── serverless/
├── templates/
    ├── vpc/
    ├── ec2/
    ├── s3/
    ├── rds/
    ├── security-groups/
    └── lambda/
```

## Configuration Types

1. **Network Configuration**
   - VPC Setup
   - Subnet Configuration
   - Route Tables
   - Internet Gateway

2. **Compute Resources**
   - EC2 Instances
   - Auto Scaling Groups
   - Launch Templates

3. **Storage Solutions**
   - S3 Buckets
   - EBS Volumes
   - EFS Configuration

4. **Security Settings**
   - Security Groups
   - IAM Roles
   - Network ACLs

5. **Database Setup**
   - RDS Instances
   - Aurora Clusters
   - DynamoDB Tables

6. **Application Services**
   - Load Balancers
   - CloudFront Distributions
   - API Gateway

7. **Monitoring**
   - CloudWatch Alarms
   - SNS Topics
   - Logging Configuration

8. **Backup & Recovery**
   - Backup Policies
   - Disaster Recovery Setup
   - Snapshot Configurations

9. **Container Services**
   - ECS Clusters
   - EKS Setup
   - ECR Repositories

10. **Serverless**
    - Lambda Functions
    - Step Functions
    - API Integrations

## Operating System Configurations
- Amazon Linux 2
- Ubuntu Server LTS
- Windows Server
- Red Hat Enterprise Linux
- CentOS

## Available Templates

### 1. Network Infrastructure (`templates/vpc/`)
- `vpc-template.yaml`: Complete VPC setup with public/private subnets
  - Multi-AZ architecture
  - Internet Gateway configuration
  - Route tables for public/private subnets
  - Network ACLs and security

### 2. Compute Resources (`templates/ec2/`)
- `ec2-template.yaml`: EC2 instance deployment
  - Multiple OS support (Amazon Linux 2, Ubuntu, RHEL, Windows, CentOS)
  - Customizable instance types
  - Security group configuration
  - EBS volume management

### 3. Storage Solutions (`templates/s3/`)
- `s3-template.yaml`: S3 bucket configuration
  - Versioning support
  - Server-side encryption
  - Lifecycle policies
  - Public access blocking
  - Security policies

### 4. Database Setup (`templates/rds/`)
- `rds-template.yaml`: RDS instance deployment
  - Multiple database engine support
  - Multi-AZ configuration
  - Automated backups
  - Security group setup
  - Subnet group configuration

### 5. Serverless (`templates/lambda/`)
- `lambda-template.yaml`: Lambda function setup
  - Multiple runtime support
  - IAM role configuration
  - CloudWatch Logs integration
  - API Gateway permissions
  - Environment variables

### 6. Container Services (`templates/ecs/`)
- `ecs-template.yaml`: ECS cluster with Fargate
  - Fargate task definitions
  - Service auto-scaling
  - Container logging
  - Load balancer integration
  - Security groups

## Security Configurations

### 1. Security Groups (`configs/security/security-groups-config.json`)
- Web server security groups
- Database security groups
- Load balancer security groups
- Custom ingress/egress rules
- Environment-specific configurations

### 2. IAM Roles (`configs/security/iam-roles-config.json`)
- Service-specific IAM roles
- Custom IAM policies
- Managed policy attachments
- Resource-based permissions
- Least privilege access configurations

### 3. WAF Rules (`configs/security/waf-config.json`)
- IP rate limiting
- Geo-matching rules
- SQL injection protection
- XSS protection
- Bad bot protection
- Custom rule sets

### 4. KMS Configuration (`configs/security/kms-config.json`)
- Application encryption keys
- Database encryption keys
- Key rotation policies
- Key usage permissions
- Service integration configurations

## Security Best Practices

### Access Control
```bash
# Deploy security groups
aws cloudformation create-stack \
    --stack-name prod-security-groups \
    --template-body file://templates/security/security-groups.yaml \
    --parameters file://configs/security/security-groups-config.json

# Deploy IAM roles
aws cloudformation create-stack \
    --stack-name prod-iam-roles \
    --template-body file://templates/security/iam-roles.yaml \
    --parameters file://configs/security/iam-roles-config.json \
    --capabilities CAPABILITY_NAMED_IAM
```

### Web Application Security
```bash
# Deploy WAF configuration
aws cloudformation create-stack \
    --stack-name prod-waf \
    --template-body file://templates/security/waf.yaml \
    --parameters file://configs/security/waf-config.json

# Deploy KMS keys
aws cloudformation create-stack \
    --stack-name prod-kms \
    --template-body file://templates/security/kms.yaml \
    --parameters file://configs/security/kms-config.json
```

### Security Guidelines
1. Implement least privilege access
2. Enable AWS CloudTrail logging
3. Use AWS Config for security rules
4. Regular security assessments
5. Implement proper key rotation
6. Monitor security events

### Compliance Requirements
1. Data encryption at rest and in transit
2. Regular access reviews
3. Security incident response plan
4. Compliance reporting
5. Audit logging

## Configuration Files

### 1. Network Configuration (`configs/network/vpc-config.json`)
- VPC CIDR configuration
- Subnet CIDR ranges
- Environment-specific settings
- Network tagging strategy

### 2. Compute Configuration (`configs/compute/ec2-config.json`)
- Instance type selections
- OS configurations
- Volume sizing
- Environment-specific instance configurations
- Resource tagging

### 3. Storage Configuration (`configs/storage/s3-config.json`)
- Bucket naming conventions
- Versioning settings
- Encryption requirements
- Lifecycle rules
- Storage class transitions

### 4. Database Configuration (`configs/database/rds-config.json`)
- Instance specifications
- Engine configurations
- Multi-AZ settings
- Backup retention policies
- Environment-specific database settings

### 5. Serverless Configuration (`configs/serverless/lambda-config.json`)
- Function configurations
- Runtime settings
- Memory allocations
- Timeout configurations
- Environment variables

### 6. Container Configuration (`configs/container/ecs-config.json`)
- Cluster settings
- Task definitions
- Container specifications
- Auto-scaling configurations
- Resource allocations

## Using Configuration Files

### Parameter Files
Create environment-specific parameter files:

```bash
# Production VPC deployment
aws cloudformation create-stack \
    --stack-name prod-vpc \
    --template-body file://templates/vpc/vpc-template.yaml \
    --parameters file://configs/network/vpc-config.json

# Development RDS deployment
aws cloudformation create-stack \
    --stack-name dev-rds \
    --template-body file://templates/rds/rds-template.yaml \
    --parameters file://configs/database/rds-config.json
```

### Configuration Management
1. Store sensitive parameters in AWS Secrets Manager
2. Use different config files for different environments
3. Implement proper version control for configs
4. Use AWS Systems Manager Parameter Store for dynamic values

### Environment-Specific Deployments
```bash
# Development Environment
aws cloudformation create-stack \
    --stack-name dev-full-stack \
    --template-body file://templates/main.yaml \
    --parameters file://configs/environments/dev.json

# Production Environment
aws cloudformation create-stack \
    --stack-name prod-full-stack \
    --template-body file://templates/main.yaml \
    --parameters file://configs/environments/prod.json
```

## Deployment Instructions

### Prerequisites
1. AWS CLI installed and configured
2. Appropriate IAM permissions
3. Python 3.x installed (for helper scripts)
4. Docker (for container deployments)

### Quick Start
1. Clone this repository
2. Navigate to the appropriate template directory
3. Customize parameters in the template
4. Deploy using AWS CLI:

```bash
# Deploy VPC
aws cloudformation create-stack \
    --stack-name my-vpc \
    --template-body file://templates/vpc/vpc-template.yaml \
    --parameters ParameterKey=EnvironmentName,ParameterValue=Production

# Deploy EC2
aws cloudformation create-stack \
    --stack-name my-ec2 \
    --template-body file://templates/ec2/ec2-template.yaml \
    --parameters ParameterKey=EnvironmentName,ParameterValue=Production

# Deploy RDS
aws cloudformation create-stack \
    --stack-name my-rds \
    --template-body file://templates/rds/rds-template.yaml \
    --parameters ParameterKey=DBPassword,ParameterValue=mypassword
```

## Best Practices
1. Always use parameter files for sensitive information
2. Implement proper tagging strategy
3. Use nested stacks for complex architectures
4. Enable termination protection for production stacks
5. Regularly update AMIs and security patches

## Usage
1. Choose the appropriate template from the templates directory
2. Customize the parameters in the corresponding config file
3. Deploy using AWS CLI or AWS Console

## Prerequisites
- AWS CLI installed and configured
- Appropriate AWS IAM permissions
- Basic understanding of AWS services

## Deployment
```bash
aws cloudformation create-stack \
    --stack-name <stack-name> \
    --template-body file://<template-file> \
    --parameters file://<parameter-file>
```
