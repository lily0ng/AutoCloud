#!/usr/bin/env python3
"""CORS Middleware"""

from flask import make_response

class CORSMiddleware:
    def __init__(self, app, allowed_origins=None):
        self.app = app
        self.allowed_origins = allowed_origins or ['*']
    
    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            headers.append(('Access-Control-Allow-Origin', self._get_origin(environ)))
            headers.append(('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'))
            headers.append(('Access-Control-Allow-Headers', 'Content-Type, Authorization'))
            headers.append(('Access-Control-Max-Age', '3600'))
            return start_response(status, headers, exc_info)
        
        if environ['REQUEST_METHOD'] == 'OPTIONS':
            custom_start_response('200 OK', [('Content-Type', 'text/plain')])
            return [b'']
        
        return self.app(environ, custom_start_response)
    
    def _get_origin(self, environ):
        origin = environ.get('HTTP_ORIGIN', '*')
        if '*' in self.allowed_origins:
            return origin
        return origin if origin in self.allowed_origins else self.allowed_origins[0]

def add_cors_headers(response):
    """Add CORS headers to Flask response"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response
