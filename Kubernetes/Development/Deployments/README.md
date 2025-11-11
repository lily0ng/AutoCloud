# Kubernetes Deployment Guide

This guide explains the Kubernetes configuration files and deployment process step by step.

## Configuration Files

1. `deployment.yaml`: Main deployment configuration
2. `service.yaml`: Service configuration for exposing the application
3. `configmap.yaml`: Application configuration
4. `secret.yaml`: Sensitive data storage

## Step-by-Step Deployment Process

### 1. Prerequisites
- Kubernetes cluster is set up and running
- kubectl is installed and configured
- Docker images are available in a container registry

### 2. Create Namespace (Optional)
```bash
kubectl create namespace my-app
kubectl config set-context --current --namespace=my-app
```

### 3. Apply Configurations
Apply the configurations in the following order:
```bash
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### 4. Verify Deployment
```bash
# Check deployment status
kubectl get deployments

# Check pods
kubectl get pods

# Check services
kubectl get services

# Check logs
kubectl logs -l app=sample-app
```

### 5. Configuration Details

#### Deployment Configuration
- Replicas: 3 pods
- Rolling Update Strategy
- Resource limits and requests
- Liveness and Readiness probes

#### Service Configuration
- Type: LoadBalancer
- Port: 80
- Selector: matches app=sample-app

#### ConfigMap
- Environment-specific configurations
- Non-sensitive application settings

#### Secrets
- Sensitive data storage
- Base64 encoded values

### 6. Scaling
```bash
# Scale deployment
kubectl scale deployment sample-app --replicas=5
```

### 7. Rolling Updates
```bash
# Update image
kubectl set image deployment/sample-app sample-app=nginx:1.20
```

### 8. Rollback
```bash
# Rollback to previous version
kubectl rollout undo deployment/sample-app
```

## Best Practices
1. Always set resource limits and requests
2. Use liveness and readiness probes
3. Implement rolling update strategy
4. Keep secrets in Kubernetes Secrets
5. Use ConfigMaps for configuration
6. Label resources appropriately
7. Use namespaces for isolation

## Monitoring
```bash
# Monitor deployment rollout
kubectl rollout status deployment/sample-app

# View deployment history
kubectl rollout history deployment/sample-app
```
