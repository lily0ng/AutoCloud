# Kubernetes Monitoring Stack

This repository contains a complete monitoring solution for Kubernetes clusters, featuring:

- Prometheus for metrics collection
- Grafana for visualization
- Alert Manager for alerting
- Node Exporter for hardware and OS metrics
- kube-state-metrics for cluster state metrics
- Custom storage monitoring
- Auto-discovery configurations

## Components

1. **Prometheus**: Main monitoring and time-series database
2. **Grafana**: Visualization and dashboarding
3. **Alert Manager**: Handling alerts and notifications
4. **Node Exporter**: System metrics collection
5. **kube-state-metrics**: Kubernetes objects metrics
6. **Storage Monitoring**: PV and PVC monitoring
7. **Service Discovery**: Auto-configuration of monitoring targets

## Installation

```bash
kubectl apply -f namespace.yaml
kubectl apply -f prometheus/
kubectl apply -f grafana/
kubectl apply -f alertmanager/
kubectl apply -f exporters/
```

## Access Services

- Grafana: http://localhost:3000 (default credentials: admin/admin)
- Prometheus: http://localhost:9090
- Alert Manager: http://localhost:9093

## Configuration

All components are configured with auto-discovery enabled for seamless monitoring of new resources.
