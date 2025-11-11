# Kubernetes Cluster Autoscaling Examples

This directory contains various Kubernetes configurations demonstrating cluster autoscaling capabilities.

## Contents

1. `cluster-autoscaler-deployment.yaml` - Main cluster autoscaler deployment
2. `node-group-autoscaling.yaml` - Node group autoscaling configuration
3. `horizontal-pod-autoscaler.yaml` - HPA configuration example
4. `vertical-pod-autoscaler.yaml` - VPA configuration example
5. `metrics-server.yaml` - Required metrics server configuration
6. `sample-deployment.yaml` - Sample application deployment with autoscaling
7. `cluster-autoscaler-rbac.yaml` - RBAC permissions for cluster autoscaler
8. `priority-expander.yaml` - Priority-based node group selection
9. `custom-metrics-config.yaml` - Custom metrics configuration for scaling
10. `autoscaling-policy.yaml` - General autoscaling policies and limits

## Prerequisites

- Kubernetes cluster (v1.19+)
- Metrics Server installed
- Proper RBAC permissions
- Cloud provider credentials configured (if using cloud provider)
