#!/usr/bin/env python3
"""Authentication and Authorization Service"""

import jwt
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional

SECRET_KEY = secrets.token_hex(32)

class AuthService:
    def __init__(self):
        self.users = {}
        self.sessions = {}
    
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, password: str, role: str = "user"):
        self.users[username] = {
            "password": self.hash_password(password),
            "role": role,
            "created_at": datetime.now()
        }
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        user = self.users.get(username)
        if user and user["password"] == self.hash_password(password):
            token = jwt.encode({
                "username": username,
                "role": user["role"],
                "exp": datetime.utcnow() + timedelta(hours=24)
            }, SECRET_KEY, algorithm="HS256")
            return token
        return None
    
    def verify_token(self, token: str) -> Optional[Dict]:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

if __name__ == "__main__":
    auth = AuthService()
    auth.create_user("admin", "admin123", "admin")
    token = auth.authenticate("admin", "admin123")
    print(f"Token: {token}")
    print(f"Verified: {auth.verify_token(token)}")
