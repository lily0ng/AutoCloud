# Kubernetes Linux Distribution Pods

This repository contains Kubernetes configurations for running multiple Linux distribution pods including Ubuntu, Debian, CentOS, and Alpine Linux. Each distribution is configured with its own deployment, service, and configuration files.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Directory Structure](#directory-structure)
- [Available Distributions](#available-distributions)
- [Quick Start](#quick-start)
- [Detailed Configuration](#detailed-configuration)
- [Usage Guide](#usage-guide)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Kubernetes cluster (v1.19+)
- kubectl CLI tool installed
- Access to container registries (Docker Hub)
- Minimum cluster resources:
  - 2 CPU cores
  - 2GB RAM
  - 10GB storage

## Directory Structure

```
Pods_and_Services/
├── README.md
├── ubuntu-deployment.yaml
├── ubuntu-config.yaml
├── ubuntu-service.yaml
├── debian-deployment.yaml
├── debian-config.yaml
├── centos-deployment.yaml
├── centos-config.yaml
├── alpine-deployment.yaml
├── alpine-config.yaml
└── linux-services.yaml
```

## Available Distributions

1. **Ubuntu 20.04**
   - Memory: 64Mi-128Mi
   - CPU: 250m-500m
   - Storage: EmptyDir volume

2. **Debian 11**
   - Memory: 64Mi-128Mi
   - CPU: 250m-500m
   - Storage: EmptyDir volume

3. **CentOS 8**
   - Memory: 128Mi-256Mi
   - CPU: 250m-500m
   - Storage: EmptyDir volume

4. **Alpine 3.15**
   - Memory: 32Mi-64Mi
   - CPU: 100m-200m
   - Storage: EmptyDir volume

## Quick Start

1. Clone this repository:
```bash
git clone <repository-url>
cd Pods_and_Services
```

2. Apply ConfigMaps:
```bash
kubectl apply -f *-config.yaml
```

3. Deploy all distributions:
```bash
kubectl apply -f *-deployment.yaml
```

4. Create services:
```bash
kubectl apply -f linux-services.yaml
```

## Detailed Configuration

### Ubuntu Configuration
```yaml
# Example ubuntu-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ubuntu-config
data:
  DEBIAN_FRONTEND: "noninteractive"
  TZ: "UTC"
```

### Resource Limits
Each distribution has specific resource limits:

```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "250m"
  limits:
    memory: "128Mi"
    cpu: "500m"
```

## Usage Guide

### Accessing Pods

1. **Ubuntu Pod**:
```bash
# Get pod name
kubectl get pods | grep ubuntu
# Access shell
kubectl exec -it <ubuntu-pod-name> -- /bin/bash
```

2. **Debian Pod**:
```bash
kubectl exec -it <debian-pod-name> -- /bin/bash
```

3. **CentOS Pod**:
```bash
kubectl exec -it <centos-pod-name> -- /bin/bash
```

4. **Alpine Pod**:
```bash
kubectl exec -it <alpine-pod-name> -- /bin/sh
```

### Working with Volumes

Each pod has a volume mounted at `/data`:
```bash
# Create test file
kubectl exec <pod-name> -- touch /data/testfile
# List files
kubectl exec <pod-name> -- ls -la /data
```

### Checking Pod Status

```bash
# Get all pods
kubectl get pods

# Get detailed pod information
kubectl describe pod <pod-name>

# Get pod logs
kubectl logs <pod-name>
```

## Monitoring and Maintenance

### Health Checks
Monitor pod health:
```bash
kubectl get pods -o wide
kubectl describe pods | grep -i status
```

### Resource Usage
Check resource consumption:
```bash
kubectl top pods
kubectl top nodes
```

### Scaling Pods
Adjust number of replicas:
```bash
kubectl scale deployment/<deployment-name> --replicas=3
```

## Troubleshooting

### Common Issues

1. **Pod in Pending State**
   - Check cluster resources:
   ```bash
   kubectl describe node
   ```
   - Verify PVC status if using persistent storage

2. **Pod in CrashLoopBackOff**
   - Check logs:
   ```bash
   kubectl logs <pod-name>
   kubectl describe pod <pod-name>
   ```

3. **Container not starting**
   - Verify image pull policy
   - Check image availability
   - Inspect container logs

### Debug Commands

```bash
# Get detailed pod information
kubectl describe pod <pod-name>

# Get pod logs
kubectl logs <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

## Best Practices

1. **Resource Management**
   - Always set resource requests and limits
   - Monitor resource usage regularly
   - Scale based on actual usage

2. **Security**
   - Use non-root users when possible
   - Implement network policies
   - Regular security updates

3. **Maintenance**
   - Keep base images updated
   - Regular backup of persistent data
   - Monitor pod health

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
