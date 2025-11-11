# Kubernetes StatefulSet Configuration and Automation

This repository contains configuration files and automation scripts for managing a Kubernetes StatefulSet deployment.

## Directory Structure

```
.
├── config/
│   └── config.yaml         # Configuration settings
├── manifests/
│   ├── statefulset.yaml    # StatefulSet definition
│   └── headless-service.yaml # Headless service definition
├── scripts/
│   ├── deploy.sh          # Deployment script
│   ├── cleanup.sh         # Cleanup script
│   ├── scale.sh          # Scaling script
│   ├── monitor.sh        # Monitoring script
│   ├── backup.sh         # Backup script
│   └── restore.sh        # Restore script
└── README.md
```

## Usage

1. Deploy the StatefulSet:
   ```bash
   ./scripts/deploy.sh
   ```

2. Scale the StatefulSet:
   ```bash
   ./scripts/scale.sh <number_of_replicas>
   ```

3. Monitor the StatefulSet:
   ```bash
   ./scripts/monitor.sh        # Single status check
   ./scripts/monitor.sh -w     # Watch mode (continuous monitoring)
   ```

4. Backup configuration:
   ```bash
   ./scripts/backup.sh
   ```

5. Restore from backup:
   ```bash
   ./scripts/restore.sh <backup_file_path>
   ```

6. Cleanup resources:
   ```bash
   ./scripts/cleanup.sh
   ```

## Configuration

Edit the `config/config.yaml` file to customize:
- Number of replicas
- Container image
- Resource requests/limits
- Storage configuration
- Network settings

## Prerequisites

- Kubernetes cluster
- kubectl configured with cluster access
- Storage class available in the cluster

## Notes

- The StatefulSet uses a headless service for network identity
- PersistentVolumeClaims are automatically created for each pod
- Default storage class is used for persistence
- Nginx is used as the default container image
