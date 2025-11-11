"""
Logging middleware for request/response tracking
"""
import logging
import time
import json
from flask import request, g
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class RequestLogger:
    """Middleware for logging HTTP requests and responses"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize middleware with Flask app"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        app.teardown_request(self.teardown_request)
    
    def before_request(self):
        """Log request details before processing"""
        g.request_id = str(uuid.uuid4())
        g.start_time = time.time()
        
        log_data = {
            'request_id': g.request_id,
            'timestamp': datetime.utcnow().isoformat(),
            'method': request.method,
            'path': request.path,
            'remote_addr': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'content_type': request.content_type,
            'content_length': request.content_length
        }
        
        # Log query parameters
        if request.args:
            log_data['query_params'] = dict(request.args)
        
        # Log request headers (exclude sensitive data)
        headers = dict(request.headers)
        sensitive_headers = ['Authorization', 'Cookie', 'X-API-Key']
        for header in sensitive_headers:
            if header in headers:
                headers[header] = '***REDACTED***'
        log_data['headers'] = headers
        
        logger.info(f"Incoming request: {json.dumps(log_data)}")
    
    def after_request(self, response):
        """Log response details after processing"""
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            
            log_data = {
                'request_id': g.get('request_id'),
                'timestamp': datetime.utcnow().isoformat(),
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'duration_ms': round(duration * 1000, 2),
                'content_length': response.content_length
            }
            
            # Add request ID to response headers
            response.headers['X-Request-ID'] = g.get('request_id')
            response.headers['X-Response-Time'] = str(duration)
            
            if response.status_code >= 400:
                logger.warning(f"Request failed: {json.dumps(log_data)}")
            else:
                logger.info(f"Request completed: {json.dumps(log_data)}")
        
        return response
    
    def teardown_request(self, exception=None):
        """Log any exceptions that occurred"""
        if exception:
            log_data = {
                'request_id': g.get('request_id'),
                'timestamp': datetime.utcnow().isoformat(),
                'method': request.method,
                'path': request.path,
                'exception': str(exception),
                'exception_type': type(exception).__name__
            }
            logger.error(f"Request exception: {json.dumps(log_data)}", exc_info=True)


def setup_logging(app, log_level=logging.INFO):
    """Setup application logging configuration"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log')
        ]
    )
    
    # Initialize request logger
    RequestLogger(app)
    
    logger.info("Logging configured successfully")
