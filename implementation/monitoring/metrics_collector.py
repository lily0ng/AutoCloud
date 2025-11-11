"""
Metrics collection service
"""
from prometheus_client import Counter, Gauge, Histogram, Summary
import psutil
import time
import logging

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Collect and expose application metrics"""
    
    def __init__(self):
        # System metrics
        self.cpu_usage = Gauge('system_cpu_usage_percent', 'CPU usage percentage')
        self.memory_usage = Gauge('system_memory_usage_bytes', 'Memory usage in bytes')
        self.disk_usage = Gauge('system_disk_usage_percent', 'Disk usage percentage')
        
        # Application metrics
        self.request_count = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
        self.request_duration = Histogram('app_request_duration_seconds', 'Request duration')
        self.error_count = Counter('app_errors_total', 'Total errors', ['type'])
        self.active_connections = Gauge('app_active_connections', 'Active connections')
        
        # Business metrics
        self.deployments_total = Counter('deployments_total', 'Total deployments', ['status'])
        self.deployment_duration = Histogram('deployment_duration_seconds', 'Deployment duration')
    
    def collect_system_metrics(self):
        """Collect system-level metrics"""
        try:
            self.cpu_usage.set(psutil.cpu_percent(interval=1))
            self.memory_usage.set(psutil.virtual_memory().used)
            self.disk_usage.set(psutil.disk_usage('/').percent)
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {str(e)}")
    
    def track_request(self, method: str, endpoint: str, duration: float):
        """Track HTTP request"""
        self.request_count.labels(method=method, endpoint=endpoint).inc()
        self.request_duration.observe(duration)
    
    def track_error(self, error_type: str):
        """Track error occurrence"""
        self.error_count.labels(type=error_type).inc()
    
    def track_deployment(self, status: str, duration: float):
        """Track deployment"""
        self.deployments_total.labels(status=status).inc()
        self.deployment_duration.observe(duration)
    
    def set_active_connections(self, count: int):
        """Set active connections count"""
        self.active_connections.set(count)
