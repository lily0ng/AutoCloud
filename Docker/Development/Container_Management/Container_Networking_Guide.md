# Container Networking Guide

## Network Types and Management

### 1. Docker Network Types
- Bridge Networks
- Host Networks
- Overlay Networks
- Macvlan Networks
- None Network

### 2. Network Commands
```bash
# Create a network
docker network create --driver bridge my-network

# List networks
docker network ls

# Connect container to network
docker network connect my-network container-name

# Inspect network
docker network inspect my-network
```

### 3. Network Configuration
```bash
# Custom bridge with subnet
docker network create \
  --driver bridge \
  --subnet=172.18.0.0/16 \
  --gateway=172.18.0.1 \
  custom-network
```

### 4. Container DNS
- Built-in DNS resolution
- Custom DNS settings
- Service discovery
- Network aliases

### 5. Load Balancing
- Docker Swarm load balancing
- External load balancers
- Health checks
- Rolling updates

### 6. Network Troubleshooting
```bash
# Debug network issues
docker network inspect network-name
docker container inspect container-name
docker logs container-name
```

### 7. Network Security
- Network isolation
- Port management
- TLS configuration
- Network policies
