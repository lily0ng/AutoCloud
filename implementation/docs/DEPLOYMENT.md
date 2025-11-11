# Deployment Guide

## Prerequisites
- Docker 20.10+
- Kubernetes 1.24+
- kubectl configured
- Helm 3.0+

## Local Development

### Setup
```bash
./scripts/setup.sh
```

### Start Services
```bash
docker-compose up -d
```

### Run Tests
```bash
./cicd/test/test.sh
```

## Docker Deployment

### Build Images
```bash
docker build -t autocloud/service-a:latest services/service-a
docker build -t autocloud/service-b:latest services/service-b
docker build -t autocloud/service-c:latest services/service-c
```

### Push to Registry
```bash
docker push autocloud/service-a:latest
docker push autocloud/service-b:latest
docker push autocloud/service-c:latest
```

## Kubernetes Deployment

### Create Namespace
```bash
kubectl create namespace production
```

### Apply Configurations
```bash
kubectl apply -f infrastructure/kubernetes/
```

### Verify Deployment
```bash
kubectl get pods -n production
kubectl get services -n production
```

### Check Logs
```bash
kubectl logs -f deployment/service-a -n production
```

## Environment Variables

### Required
- `DB_HOST` - Database host
- `DB_PASSWORD` - Database password
- `REDIS_HOST` - Redis host
- `KAFKA_BROKERS` - Kafka broker list
- `JWT_SECRET` - JWT secret key

### Optional
- `LOG_LEVEL` - Logging level (default: info)
- `PORT` - Service port (default: 8080)

## Monitoring

### Prometheus
```bash
kubectl port-forward svc/prometheus 9090:9090
```

### Grafana
```bash
kubectl port-forward svc/grafana 3000:3000
```

## Backup & Restore

### Database Backup
```bash
./database/backup/backup.sh
```

### Database Restore
```bash
./database/restore/restore.sh /path/to/backup.sql.gz
```

## Scaling

### Manual Scaling
```bash
kubectl scale deployment service-a --replicas=5 -n production
```

### Auto Scaling
```bash
kubectl autoscale deployment service-a --min=2 --max=10 --cpu-percent=80
```

## Rolling Updates
```bash
./scripts/deployment/rolling_update.sh service-a v1.2.0 production
```

## Rollback
```bash
kubectl rollout undo deployment/service-a -n production
```

## Troubleshooting

### Check Pod Status
```bash
kubectl describe pod <pod-name> -n production
```

### View Events
```bash
kubectl get events -n production --sort-by='.lastTimestamp'
```

### Debug Container
```bash
kubectl exec -it <pod-name> -n production -- /bin/sh
```
