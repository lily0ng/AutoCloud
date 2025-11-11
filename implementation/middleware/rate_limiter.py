"""
Rate limiting middleware for API protection
"""
from flask import request, jsonify
from functools import wraps
import time
from collections import defaultdict
import threading


class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, rate=100, per=60):
        """
        Initialize rate limiter
        
        Args:
            rate: Number of requests allowed
            per: Time period in seconds
        """
        self.rate = rate
        self.per = per
        self.allowance = defaultdict(lambda: rate)
        self.last_check = defaultdict(lambda: time.time())
        self.lock = threading.Lock()
    
    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed"""
        with self.lock:
            current = time.time()
            time_passed = current - self.last_check[key]
            self.last_check[key] = current
            
            self.allowance[key] += time_passed * (self.rate / self.per)
            
            if self.allowance[key] > self.rate:
                self.allowance[key] = self.rate
            
            if self.allowance[key] < 1.0:
                return False
            else:
                self.allowance[key] -= 1.0
                return True
    
    def get_remaining(self, key: str) -> int:
        """Get remaining requests for key"""
        return int(self.allowance.get(key, self.rate))


# Global rate limiter instances
default_limiter = RateLimiter(rate=100, per=60)
strict_limiter = RateLimiter(rate=10, per=60)


def rate_limit(limiter=None):
    """Rate limiting decorator"""
    if limiter is None:
        limiter = default_limiter
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client identifier (IP or user ID)
            client_id = request.headers.get('X-Client-ID') or request.remote_addr
            
            if not limiter.is_allowed(client_id):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Maximum {limiter.rate} requests per {limiter.per} seconds',
                    'retry_after': limiter.per
                }), 429
            
            # Add rate limit headers
            response = f(*args, **kwargs)
            if isinstance(response, tuple):
                response_obj, status_code = response
            else:
                response_obj = response
                status_code = 200
            
            if hasattr(response_obj, 'headers'):
                response_obj.headers['X-RateLimit-Limit'] = str(limiter.rate)
                response_obj.headers['X-RateLimit-Remaining'] = str(limiter.get_remaining(client_id))
                response_obj.headers['X-RateLimit-Reset'] = str(int(time.time() + limiter.per))
            
            return response_obj, status_code
        
        return decorated_function
    return decorator


def ip_rate_limit(rate=100, per=60):
    """IP-based rate limiting decorator"""
    limiter = RateLimiter(rate=rate, per=per)
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip_address = request.remote_addr
            
            if not limiter.is_allowed(ip_address):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Maximum {rate} requests per {per} seconds from your IP',
                    'retry_after': per
                }), 429
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
