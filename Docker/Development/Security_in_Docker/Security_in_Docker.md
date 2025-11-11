# Docker Security Best Practices and Configurations

## Table of Contents
1. [Container Security Fundamentals](#container-security-fundamentals)
2. [Docker Daemon Security](#docker-daemon-security)
3. [Image Security](#image-security)
4. [Runtime Security](#runtime-security)
5. [Network Security](#network-security)
6. [Access Control and Authentication](#access-control-and-authentication)
7. [Monitoring and Logging](#monitoring-and-logging)

## Container Security Fundamentals

### 1. Use Official Base Images
```dockerfile
# Good Practice
FROM ubuntu:22.04
# Instead of using untrusted images
```

### 2. Run Containers as Non-Root
```dockerfile
# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
```

### 3. Set Resource Limits
```yaml
# docker-compose.yml
services:
  app:
    mem_limit: 512m
    cpus: 0.5
    pids_limit: 100
```

## Docker Daemon Security

### 1. Daemon Configuration
Create or edit `/etc/docker/daemon.json`:
```json
{
  "userns-remap": "default",
  "live-restore": true,
  "icc": false,
  "no-new-privileges": true,
  "seccomp-profile": "/etc/docker/seccomp-profile.json",
  "selinux-enabled": true,
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### 2. TLS Configuration
```bash
# Generate CA, server and client keys
mkdir -p ~/.docker/tls
cd ~/.docker/tls
openssl genrsa -aes256 -out ca-key.pem 4096
openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem
```

## Image Security

### 1. Scanning Images
```bash
# Use Docker Scan
docker scan myimage:latest

# Use Trivy
trivy image myimage:latest
```

### 2. Multi-Stage Builds
```dockerfile
# Build stage
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main

# Final stage
FROM alpine:3.18
COPY --from=builder /app/main /
USER nonroot
ENTRYPOINT ["/main"]
```

## Runtime Security

### 1. Security Options
```yaml
# docker-compose.yml
services:
  secure-app:
    security_opt:
      - no-new-privileges:true
      - seccomp:seccomp-profile.json
      - apparmor:docker-default
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### 2. Read-Only Root Filesystem
```dockerfile
# Enable read-only root filesystem
VOLUME ["/tmp", "/var/run"]
RUN chmod 1777 /tmp
```

## Network Security

### 1. Network Isolation
```yaml
# docker-compose.yml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true

services:
  webapp:
    networks:
      - frontend
  database:
    networks:
      - backend
```

### 2. Network Encryption
```yaml
# docker-compose.yml
services:
  app:
    networks:
      mynet:
        ipv4_address: 172.20.0.2
networks:
  mynet:
    driver: overlay
    driver_opts:
      encrypted: "true"
```

## Access Control and Authentication

### 1. Docker Content Trust
```bash
# Enable Docker Content Trust
export DOCKER_CONTENT_TRUST=1

# Sign images during push
docker trust sign myregistry.azurecr.io/myimage:latest
```

### 2. Role-Based Access Control (RBAC)
```yaml
# Example Docker EE UCP configuration
{
  "role_name": "dev-role",
  "operations": [
    {
      "resource_type": "container",
      "resource_name": "dev-*",
      "actions": ["create", "view", "start", "stop"]
    }
  ]
}
```

## Monitoring and Logging

### 1. Audit Logging
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3",
    "labels": "production_status",
    "env": "os,customer"
  }
}
```

### 2. Container Monitoring
```yaml
# docker-compose.yml with monitoring
services:
  app:
    labels:
      - "monitoring=true"
    logging:
      driver: "json-file"
      options:
        max-size: "200k"
        max-file: "10"
```

## Security Checklist

1. ✅ Use minimal base images
2. ✅ Implement least privilege principle
3. ✅ Enable Docker Content Trust
4. ✅ Regular security scanning
5. ✅ Network segmentation
6. ✅ Resource limitations
7. ✅ Logging and monitoring
8. ✅ Regular updates and patches
9. ✅ Secure configuration files
10. ✅ Access control implementation

## Additional Security Tools

1. **Clair**: Open source container vulnerability scanner
2. **Aqua Security**: Commercial container security platform
3. **Anchore**: Container security and compliance platform
4. **Falco**: Runtime security monitoring
5. **Docker Bench Security**: Security assessment tool

Remember to regularly update your Docker engine and all containers to ensure you have the latest security patches and features.
