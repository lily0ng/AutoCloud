from typing import Dict, Optional
import hashlib
import hmac
import time
import secrets
import redis
from datetime import datetime, timedelta

class APIAuthManager:
    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port)
        
    def generate_api_key(self, client_id: str, expiry_days: int = 365) -> Dict[str, str]:
        api_key = secrets.token_urlsafe(32)
        api_secret = secrets.token_urlsafe(64)
        
        # Store in Redis with expiration
        key_data = {
            'client_id': client_id,
            'api_secret': api_secret,
            'created_at': datetime.utcnow().isoformat()
        }
        self.redis_client.hmset(f"api_key:{api_key}", key_data)
        self.redis_client.expire(f"api_key:{api_key}", expiry_days * 24 * 3600)
        
        return {
            'api_key': api_key,
            'api_secret': api_secret,
            'client_id': client_id
        }
        
    def validate_request(self, api_key: str, signature: str, timestamp: str, 
                        payload: str = '') -> bool:
        # Check if API key exists
        key_data = self.redis_client.hgetall(f"api_key:{api_key}")
        if not key_data:
            return False
            
        # Verify timestamp is within acceptable range (5 minutes)
        try:
            request_time = int(timestamp)
            current_time = int(time.time())
            if abs(current_time - request_time) > 300:  # 5 minutes
                return False
        except ValueError:
            return False
            
        # Verify signature
        api_secret = key_data.get(b'api_secret').decode()
        message = f"{timestamp}{payload}"
        expected_signature = hmac.new(
            api_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
        
    def revoke_api_key(self, api_key: str) -> bool:
        return bool(self.redis_client.delete(f"api_key:{api_key}"))
        
    def get_client_id(self, api_key: str) -> Optional[str]:
        key_data = self.redis_client.hgetall(f"api_key:{api_key}")
        if key_data and b'client_id' in key_data:
            return key_data[b'client_id'].decode()
        return None
        
    def update_api_key_expiry(self, api_key: str, expiry_days: int) -> bool:
        if self.redis_client.exists(f"api_key:{api_key}"):
            return bool(self.redis_client.expire(
                f"api_key:{api_key}", 
                expiry_days * 24 * 3600
            ))
        return False
