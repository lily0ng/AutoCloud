#!/bin/bash
# Prometheus Monitoring Setup

set -e

NAMESPACE=${NAMESPACE:-"monitoring"}
RETENTION=${RETENTION:-"30d"}
STORAGE_SIZE=${STORAGE_SIZE:-"50Gi"}

echo "📊 Setting up Prometheus monitoring stack..."

# Add Prometheus Helm repo
echo "📦 Adding Prometheus Helm repository..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Create namespace
echo "📁 Creating namespace: $NAMESPACE"
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Install Prometheus Operator
echo "🔧 Installing Prometheus Operator..."
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
    --namespace "$NAMESPACE" \
    --set prometheus.prometheusSpec.retention="$RETENTION" \
    --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage="$STORAGE_SIZE" \
    --set grafana.enabled=true \
    --set grafana.adminPassword=admin \
    --set alertmanager.enabled=true \
    --wait

# Create ServiceMonitor for custom apps
echo "📝 Creating ServiceMonitor..."
cat <<EOF | kubectl apply -f -
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-metrics
  namespace: $NAMESPACE
spec:
  selector:
    matchLabels:
      app: my-app
  endpoints:
  - port: metrics
    interval: 30s
EOF

# Create PrometheusRule for alerts
echo "🚨 Creating alert rules..."
cat <<EOF | kubectl apply -f -
apiVersion: monitoring.coreos.com/v1
kind:PrometheusRule
metadata:
  name: app-alerts
  namespace: $NAMESPACE
spec:
  groups:
  - name: app
    interval: 30s
    rules:
    - alert: HighCPUUsage
      expr: rate(container_cpu_usage_seconds_total[5m]) > 0.8
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High CPU usage detected"
    - alert: HighMemoryUsage
      expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "High memory usage detected"
EOF

echo ""
echo "✅ Prometheus stack installed successfully!"
echo ""
echo "📝 Access Information:"
echo "  Prometheus: kubectl port-forward -n $NAMESPACE svc/prometheus-kube-prometheus-prometheus 9090:9090"
echo "  Grafana: kubectl port-forward -n $NAMESPACE svc/prometheus-grafana 3000:80"
echo "  AlertManager: kubectl port-forward -n $NAMESPACE svc/prometheus-kube-prometheus-alertmanager 9093:9093"
echo ""
echo "  Grafana credentials: admin / admin"
echo ""
echo "🎯 Next steps:"
echo "  1. Access Grafana and import dashboards"
echo "  2. Configure AlertManager notification channels"
echo "  3. Add custom ServiceMonitors for your applications"
