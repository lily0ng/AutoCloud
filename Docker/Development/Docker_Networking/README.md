# Docker Networking Guide

This guide covers comprehensive information about Docker networking, including network configuration, troubleshooting, port forwarding, proxy settings, and IP address management.

## Table of Contents
- [Network Types](#network-types)
- [Basic Network Commands](#basic-network-commands)
- [Port Forwarding](#port-forwarding)
- [Network Configuration](#network-configuration)
- [Proxy Settings](#proxy-settings)
- [IP Address Management](#ip-address-management)
- [Common Error Solutions](#common-error-solutions)

## Network Types

Docker provides several built-in network drivers:

1. **bridge**: The default network driver. Used when multiple containers need to communicate on the same Docker host.
```bash
# Create a bridge network
docker network create --driver bridge my_network

# Connect container to network
docker network connect my_network container_name
```

2. **host**: Container shares the host's networking namespace.
```bash
# Run container with host networking
docker run --network host my_container
```

3. **none**: Disables networking for container.
```bash
docker run --network none my_container
```

4. **overlay**: For communication between containers across multiple Docker hosts.
```bash
# Create overlay network
docker network create --driver overlay my_overlay_network
```

## Basic Network Commands

Essential Docker network commands:

```bash
# List networks
docker network ls

# Inspect network
docker network inspect network_name

# Remove network
docker network rm network_name

# Disconnect container from network
docker network disconnect network_name container_name
```

## Port Forwarding

### Basic Port Forwarding
```bash
# Format: docker run -p host_port:container_port
docker run -p 8080:80 nginx

# Multiple port forwarding
docker run -p 8080:80 -p 443:443 nginx

# Bind to specific interface
docker run -p 127.0.0.1:8080:80 nginx
```

### Dynamic Port Mapping
```bash
# Let Docker assign random host port
docker run -p 80 nginx

# Check assigned ports
docker port container_name
```

## Network Configuration

### Custom Bridge Network Configuration
```bash
# Create network with custom subnet
docker network create --subnet=172.18.0.0/16 custom_network

# Create network with gateway
docker network create --subnet=172.18.0.0/16 --gateway=172.18.0.1 custom_network

# Assign static IP to container
docker run --network custom_network --ip 172.18.0.10 nginx
```

### DNS Configuration
```bash
# Custom DNS
docker run --dns 8.8.8.8 nginx

# Add DNS search domains
docker run --dns-search example.com nginx
```

## Proxy Settings

### Container Level Proxy
```bash
# Set HTTP proxy
docker run -e HTTP_PROXY="http://proxy.example.com:8080" nginx

# Set HTTPS proxy
docker run -e HTTPS_PROXY="https://proxy.example.com:8080" nginx

# No proxy for specific addresses
docker run -e NO_PROXY="localhost,127.0.0.1" nginx
```

### Docker Daemon Proxy
Create or modify `/etc/docker/daemon.json`:
```json
{
    "proxies": {
        "http-proxy": "http://proxy.example.com:8080",
        "https-proxy": "https://proxy.example.com:8080",
        "no-proxy": "localhost,127.0.0.1"
    }
}
```

## IP Address Management

### Static IP Assignment
```bash
# Create network with specific subnet
docker network create --subnet=172.20.0.0/16 static_network

# Run container with static IP
docker run --network static_network --ip 172.20.0.2 nginx
```

### IP Range Management
```bash
# Create network with IP range
docker network create --subnet=172.20.0.0/16 --ip-range=172.20.5.0/24 range_network
```

## Common Error Solutions

### Network Connectivity Issues

1. **Container Can't Connect to Internet**
   - Check DNS settings
   ```bash
   docker run --dns 8.8.8.8 nginx
   ```
   - Verify host network connectivity
   - Check iptables rules

2. **Port Conflicts**
   - List used ports
   ```bash
   docker port container_name
   netstat -tulpn
   ```
   - Change port mapping

3. **Container Name Resolution Fails**
   - Ensure containers are on same network
   - Check DNS configuration
   - Use docker network inspect

### Troubleshooting Commands
```bash
# Check container networking
docker inspect container_name | grep -i ip

# View container logs
docker logs container_name

# Enter container for network debugging
docker exec -it container_name /bin/bash
```

## Best Practices

1. Use custom bridge networks for container isolation
2. Implement proper network segmentation
3. Use meaningful network names
4. Document port mappings
5. Regularly clean unused networks
6. Monitor network usage
7. Implement proper security measures

## Security Considerations

1. Avoid exposing unnecessary ports
2. Use host network mode sparingly
3. Implement network policies
4. Regular security audits
5. Keep Docker updated

Remember to always follow security best practices and regularly update your Docker installation for the latest security patches and features.
