# Cloud Infrastructure Helm Charts

<img src="https://helm.sh/img/helm.svg" width="150" height="150" alt="Helm Logo">

## Overview
This repository contains Helm charts for deploying and managing various microservices in a Kubernetes cluster. The charts are configured for both development and production environments.

## Structure
```
helm-charts/
├── charts/
│   ├── service1/
│   ├── service2/
│   └── ...
├── config/
│   ├── dev/
│   ├── prod/
│   └── staging/
└── values/
```

## Services Included
1. API Gateway Service
2. Authentication Service
3. User Service
4. Notification Service
5. Monitoring Service
6. Logging Service
7. Database Service
8. Cache Service
9. Message Queue Service
10. Storage Service

## Environment Configurations
### Development
- Lightweight resources for local development
- Single replica deployments
- Hot reload enabled
- Mock services available
- Debug endpoints enabled
- Verbose logging
- Self-signed certificates
- Sample data included
- No replication or high availability
- Minimal security constraints

### Production
- High availability setup
- Multiple replicas for critical services
- Production-grade resource allocation
- Full monitoring and alerting
- Automated backups
- Strict security policies

### Staging
- Moderate resource allocation
- Single replica for most services
- Debug-level logging enabled
- Staging SSL certificates
- Test data and configurations

## Configuration Files
### Database Configuration
- Connection pools and settings
- Backup schedules
- Replication configuration
- Resource allocation
- Security settings

### Network Configuration
- Ingress settings
- Service mesh configuration
- Load balancer setup
- Network policies
- DNS configuration

### Monitoring Configuration
- Prometheus settings
- Grafana dashboards
- Alert manager rules
- Logging configuration
- Tracing setup

## Values Structure
```
values/
├── production-values.yaml
├── staging-values.yaml
├── development-values.yaml
└── common-values.yaml
```

## Usage
### Installing Charts
```bash
# Add the repository
helm repo add my-charts https://[your-repo-url]

# Update repositories
helm repo update

# Install a chart in staging
helm install [release-name] my-charts/[chart-name] -f values/staging-values.yaml

# Install a chart in production
helm install [release-name] my-charts/[chart-name] -f values/production-values.yaml

# Install a chart in development
helm install [release-name] my-charts/[chart-name] -f values/development-values.yaml
```

### Upgrading Charts
```bash
helm upgrade [release-name] my-charts/[chart-name] -f values/[environment]-values.yaml
```

### Rollback
```bash
helm rollback [release-name] [revision]
```

## Maintenance
- Regular updates to chart versions
- Security patches
- Configuration reviews
- Performance monitoring
- Backup verification

## Prerequisites
- Kubernetes 1.19+
- Helm 3.0+
- kubectl configured to communicate with your cluster

## Installation
```bash
helm repo add my-repo https://[your-repo-url]
helm repo update
helm install [release-name] my-repo/[chart-name]
```

## Configuration
Refer to the individual chart's README for specific configuration options.

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details
