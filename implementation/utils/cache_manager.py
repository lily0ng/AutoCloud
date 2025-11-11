"""
Cache management utility with Redis support
"""
import redis
import json
import pickle
from typing import Any, Optional
from functools import wraps
import hashlib


class CacheManager:
    """Redis cache manager"""
    
    def __init__(self, host='localhost', port=6379, db=0, ttl=3600):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=False)
        self.default_ttl = ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        value = self.client.get(key)
        if value:
            return pickle.loads(value)
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache"""
        ttl = ttl or self.default_ttl
        self.client.setex(key, ttl, pickle.dumps(value))
    
    def delete(self, key: str):
        """Delete key from cache"""
        self.client.delete(key)
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        return self.client.exists(key) > 0
    
    def clear_pattern(self, pattern: str):
        """Clear all keys matching pattern"""
        for key in self.client.scan_iter(match=pattern):
            self.client.delete(key)


def cache_result(ttl=3600, key_prefix=''):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = CacheManager()
            
            # Generate cache key
            key_data = f"{key_prefix}:{func.__name__}:{args}:{kwargs}"
            cache_key = hashlib.md5(key_data.encode()).hexdigest()
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator
