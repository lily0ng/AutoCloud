#!/usr/bin/env python3
"""Authentication Middleware"""

from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime

SECRET_KEY = "your-secret-key"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if request.user.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    
    return decorated

def rate_limit(max_requests=100, window=60):
    """Rate limiting decorator"""
    requests_dict = {}
    
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = datetime.now().timestamp()
            
            if client_ip not in requests_dict:
                requests_dict[client_ip] = []
            
            requests_dict[client_ip] = [
                t for t in requests_dict[client_ip]
                if current_time - t < window
            ]
            
            if len(requests_dict[client_ip]) >= max_requests:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            requests_dict[client_ip].append(current_time)
            return f(*args, **kwargs)
        
        return decorated
    return decorator
