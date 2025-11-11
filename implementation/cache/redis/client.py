#!/usr/bin/env python3
"""Redis Cache Client Implementation"""

import redis
import json
import pickle
from typing import Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=False
        )
        logger.info(f"Connected to Redis at {host}:{port}")
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        serialized = pickle.dumps(value)
        self.client.setex(key, ttl, serialized)
        logger.debug(f"Set key: {key} with TTL: {ttl}s")
    
    def get(self, key: str) -> Optional[Any]:
        data = self.client.get(key)
        if data:
            return pickle.loads(data)
        return None
    
    def delete(self, key: str):
        self.client.delete(key)
        logger.debug(f"Deleted key: {key}")
    
    def exists(self, key: str) -> bool:
        return self.client.exists(key) > 0
    
    def increment(self, key: str, amount: int = 1) -> int:
        return self.client.incrby(key, amount)
    
    def get_ttl(self, key: str) -> int:
        return self.client.ttl(key)
    
    def flush_all(self):
        self.client.flushall()
        logger.warning("Flushed all Redis data")

if __name__ == "__main__":
    cache = RedisCache()
    cache.set("user:1", {"name": "John", "age": 30}, ttl=60)
    user = cache.get("user:1")
    print(f"Cached user: {user}")
