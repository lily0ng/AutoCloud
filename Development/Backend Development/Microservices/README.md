# Cloud-Native Microservices Architecture

This project implements a cloud-native microservices architecture with the following components:

## Services
- User Service (Port: 8081)
- Product Service (Port: 8082)
- Order Service (Port: 8083)
- API Gateway (Port: 8080)
- Service Discovery (Eureka) (Port: 8761)

## Monitoring & Observability
- Prometheus (Port: 9090)
- Grafana (Port: 3000)

## Infrastructure
- PostgreSQL Database
- Kubernetes Deployment
- Istio Service Mesh
- CI/CD Pipeline (GitHub Actions)

## Getting Started

1. Build the services:
```bash
mvn clean package
```

2. Start the services:
```bash
docker-compose up -d
```

3. Access the services:
- API Gateway: http://localhost:8080
- Eureka Dashboard: http://localhost:8761
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Deployment

The project includes Kubernetes configurations for cloud deployment:
```bash
kubectl apply -f k8s/
```

## Monitoring

Access Grafana (http://localhost:3000) and import the provided dashboards for monitoring:
- Service Health
- JVM Metrics
- API Gateway Metrics

## Service Mesh

Istio configurations are provided for:
- Traffic Management
- Security
- Observability

## CI/CD

The GitHub Actions workflow automates:
- Building
- Testing
- Docker image creation
- Kubernetes deployment
