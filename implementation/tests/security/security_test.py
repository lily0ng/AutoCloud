#!/usr/bin/env python3
"""Security Testing Suite"""

import requests
import unittest

class SecurityTests(unittest.TestCase):
    
    def setUp(self):
        self.base_url = "http://localhost:8080"
    
    def test_sql_injection(self):
        """Test SQL injection protection"""
        payloads = [
            "' OR '1'='1",
            "1' UNION SELECT NULL--",
            "admin'--",
        ]
        
        for payload in payloads:
            response = requests.get(f"{self.base_url}/api/v1/users?id={payload}")
            self.assertNotEqual(response.status_code, 200, 
                              f"SQL injection vulnerability with payload: {payload}")
    
    def test_xss_protection(self):
        """Test XSS protection"""
        payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
        ]
        
        for payload in payloads:
            response = requests.post(f"{self.base_url}/api/v1/process", 
                                    json={"data": payload})
            if response.status_code == 200:
                self.assertNotIn("<script>", response.text.lower())
    
    def test_authentication_required(self):
        """Test authentication requirement"""
        response = requests.get(f"{self.base_url}/api/v1/users")
        self.assertIn(response.status_code, [401, 403], 
                     "Endpoint should require authentication")
    
    def test_rate_limiting(self):
        """Test rate limiting"""
        responses = []
        for _ in range(150):
            response = requests.get(f"{self.base_url}/health")
            responses.append(response.status_code)
        
        self.assertIn(429, responses, "Rate limiting should be enforced")
    
    def test_cors_headers(self):
        """Test CORS headers"""
        response = requests.options(f"{self.base_url}/api/v1/users")
        self.assertIn('Access-Control-Allow-Origin', response.headers)

if __name__ == '__main__':
    unittest.main()
