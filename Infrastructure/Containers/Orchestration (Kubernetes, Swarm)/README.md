# Container Orchestration Setup (Kubernetes & Docker Swarm)

This repository contains automation scripts and configuration files for setting up and managing container orchestration using both Kubernetes and Docker Swarm.

## Directory Structure
```
.
├── kubernetes/
│   ├── configs/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── ingress.yaml
│   │   ├── configmap.yaml
│   │   ├── secret.yaml
│   │   └── rbac.yaml
│   └── scripts/
│       ├── k8s-setup.sh
│       └── k8s-cleanup.sh
└── swarm/
    ├── configs/
    │   ├── docker-compose.yaml
    │   └── stack-config.yaml
    └── scripts/
        ├── swarm-setup.sh
        └── swarm-cleanup.sh
```

## Prerequisites

- Docker Engine 24.0.0+
- kubectl v1.28+
- minikube v1.32+ (for local development)
- helm v3.0+ (optional, for package management)

## Quick Start

### Kubernetes Setup

1. Initialize Kubernetes cluster:
```bash
cd kubernetes/scripts
chmod +x k8s-setup.sh
./k8s-setup.sh
```

2. Deploy basic infrastructure:
```bash
kubectl apply -f ../configs/
```

3. Verify deployment:
```bash
kubectl get pods,svc,ing
```

### Docker Swarm Setup

1. Initialize Swarm cluster:
```bash
cd swarm/scripts
chmod +x swarm-setup.sh
./swarm-setup.sh
```

2. Deploy stack:
```bash
docker stack deploy -c ../configs/docker-compose.yaml myapp
```

3. Verify deployment:
```bash
docker stack ps myapp
```

## Configuration Details

### Kubernetes Configurations

1. `deployment.yaml`: Defines application deployments with replicas and container specs
2. `service.yaml`: Exposes deployments through ClusterIP or LoadBalancer
3. `ingress.yaml`: Configures HTTP/HTTPS routing
4. `configmap.yaml`: Stores non-sensitive configuration data
5. `secret.yaml`: Manages sensitive information (credentials, tokens)
6. `rbac.yaml`: Defines role-based access control policies

### Docker Swarm Configurations

1. `docker-compose.yaml`: Defines services, networks, and volumes
2. `stack-config.yaml`: Contains environment-specific configurations

## Automation Scripts

### Kubernetes Scripts

- `k8s-setup.sh`: 
  - Initializes Kubernetes cluster
  - Sets up networking (Calico/Flannel)
  - Configures metrics server
  - Deploys basic monitoring

- `k8s-cleanup.sh`:
  - Removes all deployments
  - Cleans up persistent volumes
  - Resets cluster state

### Swarm Scripts

- `swarm-setup.sh`:
  - Initializes Swarm cluster
  - Configures overlay networks
  - Sets up node labels
  - Deploys monitoring stack

- `swarm-cleanup.sh`:
  - Removes all stacks
  - Leaves swarm cluster
  - Cleans up volumes

## Monitoring & Maintenance

### Kubernetes
- Access Dashboard: `kubectl proxy`
- View logs: `kubectl logs -f <pod-name>`
- Scale deployment: `kubectl scale deployment/<name> --replicas=<number>`

### Docker Swarm
- View services: `docker service ls`
- Scale service: `docker service scale <service-name>=<number>`
- View logs: `docker service logs <service-name>`

## Troubleshooting

1. Check node status:
   - Kubernetes: `kubectl get nodes`
   - Swarm: `docker node ls`

2. View system events:
   - Kubernetes: `kubectl get events --sort-by=.metadata.creationTimestamp`
   - Swarm: `docker events`

3. Common issues:
   - Network connectivity
   - Resource constraints
   - Configuration errors
   - Permission issues

## Security Considerations

1. Always use RBAC policies
2. Implement network policies
3. Regular security updates
4. Use secrets management
5. Enable audit logging

## Best Practices

1. Use namespaces for isolation
2. Implement resource limits
3. Regular backup of configurations
4. Monitor cluster health
5. Use rolling updates
