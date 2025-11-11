#!/usr/bin/env python3
"""Metrics Collector for Monitoring"""

import time
import psutil
import logging
from prometheus_client import Counter, Gauge, Histogram, start_http_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define metrics
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
cpu_usage = Gauge('system_cpu_usage_percent', 'CPU usage percentage')
memory_usage = Gauge('system_memory_usage_percent', 'Memory usage percentage')
disk_usage = Gauge('system_disk_usage_percent', 'Disk usage percentage')

class MetricsCollector:
    def __init__(self, port=9090):
        self.port = port
        
    def collect_system_metrics(self):
        """Collect system metrics"""
        while True:
            cpu_usage.set(psutil.cpu_percent(interval=1))
            memory_usage.set(psutil.virtual_memory().percent)
            disk_usage.set(psutil.disk_usage('/').percent)
            time.sleep(10)
    
    def record_request(self, method, endpoint, status, duration):
        """Record HTTP request metrics"""
        request_count.labels(method=method, endpoint=endpoint, status=status).inc()
        request_duration.observe(duration)
    
    def start(self):
        """Start metrics server"""
        start_http_server(self.port)
        logger.info(f"Metrics server started on port {self.port}")
        self.collect_system_metrics()

if __name__ == "__main__":
    collector = MetricsCollector()
    collector.start()
