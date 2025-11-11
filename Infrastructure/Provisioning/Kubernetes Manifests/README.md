<img src="https://kubernetes.io/images/kubernetes-horizontal-color.png" alt="Kubernetes Logo" width="400"/>

# Kubernetes Infrastructure Setup

This repository contains Kubernetes manifests and automation scripts for setting up a complete cloud infrastructure.

## Directory Structure

```
.
├── apps/
│   ├── web-app.yaml
│   └── database.yaml
├── config/
├── core/
├── monitoring/
│   └── prometheus-config.yaml
├── namespaces/
│   └── namespaces.yaml
├── network/
│   └── network-policies.yaml
├── service-mesh/
│   └── istio-config.yaml
├── storage/
│   └── storage-class.yaml
└── setup.sh
```

## Prerequisites

- Kubernetes cluster (1.19+)
- kubectl configured to connect to your cluster
- Helm (optional, for additional package management)

## Setup Instructions

1. Clone this repository
2. Make the setup script executable:
   ```bash
   chmod +x setup.sh
   ```
3. Run the setup script:
   ```bash
   ./setup.sh
   ```

## Components

- **Namespaces**: Separate environments for production, staging, development, monitoring, and logging
- **Storage**: Configuration for different storage classes
- **Network Policies**: Basic network security policies
- **Service Mesh**: Istio configuration for service mesh capabilities
- **Monitoring**: Prometheus configuration for monitoring
- **Applications**: Sample web application and database deployments

## Configuration

Modify the yaml files in each directory according to your needs before running the setup script.

## Security Considerations

- Update the database passwords in a secure manner
- Review and adjust network policies
- Configure appropriate resource limits
- Set up proper RBAC policies

## Maintenance

Regular updates and maintenance:

1. Keep your Kubernetes version updated
2. Regularly update application images
3. Monitor resource usage
4. Backup critical data
5. Review and update security policies
