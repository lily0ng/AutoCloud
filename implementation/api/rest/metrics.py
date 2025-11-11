"""
Metrics API for Prometheus integration
"""
from flask import Blueprint, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time

metrics_bp = Blueprint('metrics', __name__)

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Number of active HTTP requests'
)

ERROR_COUNT = Counter(
    'http_errors_total',
    'Total HTTP errors',
    ['method', 'endpoint', 'error_type']
)


@metrics_bp.route('/metrics', methods=['GET'])
def metrics():
    """Expose metrics in Prometheus format"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


def track_request(method, endpoint, status_code):
    """Track request metrics"""
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status_code).inc()


def track_error(method, endpoint, error_type):
    """Track error metrics"""
    ERROR_COUNT.labels(method=method, endpoint=endpoint, error_type=error_type).inc()


class MetricsMiddleware:
    """Middleware to track request metrics"""
    
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        start_time = time.time()
        ACTIVE_REQUESTS.inc()
        
        def custom_start_response(status, headers, exc_info=None):
            status_code = int(status.split()[0])
            method = environ.get('REQUEST_METHOD')
            path = environ.get('PATH_INFO')
            
            duration = time.time() - start_time
            REQUEST_DURATION.labels(method=method, endpoint=path).observe(duration)
            REQUEST_COUNT.labels(method=method, endpoint=path, status=status_code).inc()
            
            ACTIVE_REQUESTS.dec()
            return start_response(status, headers, exc_info)
        
        return self.app(environ, custom_start_response)
