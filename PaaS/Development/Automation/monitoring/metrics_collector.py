from prometheus_client import start_http_server, Counter, Gauge, Histogram
import psutil
import time
import logging
from typing import Dict, Any

class MetricsCollector:
    def __init__(self, port: int = 8000):
        self.port = port
        self.logger = logging.getLogger(__name__)
        
        # Define metrics
        self.cpu_usage = Gauge('system_cpu_usage', 'Current CPU usage percentage')
        self.memory_usage = Gauge('system_memory_usage', 'Current memory usage percentage')
        self.disk_usage = Gauge('system_disk_usage', 'Current disk usage percentage')
        self.request_count = Counter('http_requests_total', 'Total HTTP requests')
        self.request_latency = Histogram(
            'http_request_duration_seconds',
            'HTTP request latency in seconds'
        )

    def start_server(self):
        try:
            start_http_server(self.port)
            self.logger.info(f"Metrics server started on port {self.port}")
        except Exception as e:
            self.logger.error(f"Failed to start metrics server: {str(e)}")
            raise

    def collect_system_metrics(self):
        try:
            # CPU usage
            self.cpu_usage.set(psutil.cpu_percent())
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.memory_usage.set(memory.percent)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            self.disk_usage.set(disk.percent)
        except Exception as e:
            self.logger.error(f"Failed to collect system metrics: {str(e)}")
            raise

    def record_request(self, duration: float):
        """Record an HTTP request and its duration"""
        self.request_count.inc()
        self.request_latency.observe(duration)

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current metric values"""
        return {
            'cpu_usage': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent
        }

    def run_metrics_collection(self, interval: int = 60):
        """Run continuous metrics collection"""
        while True:
            try:
                self.collect_system_metrics()
                time.sleep(interval)
            except Exception as e:
                self.logger.error(f"Error in metrics collection loop: {str(e)}")
                time.sleep(5)  # Wait before retrying
