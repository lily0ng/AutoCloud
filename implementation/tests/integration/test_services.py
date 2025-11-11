#!/usr/bin/env python3
"""Integration tests for services"""

import unittest
import requests
import time

class TestServiceIntegration(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.base_urls = {
            'service_a': 'http://localhost:8080',
            'service_b': 'http://localhost:8081',
            'service_c': 'http://localhost:8082',
        }
        time.sleep(2)
    
    def test_service_a_health(self):
        response = requests.get(f"{self.base_urls['service_a']}/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
    
    def test_service_b_health(self):
        response = requests.get(f"{self.base_urls['service_b']}/health")
        self.assertEqual(response.status_code, 200)
    
    def test_service_c_health(self):
        response = requests.get(f"{self.base_urls['service_c']}/health")
        self.assertEqual(response.status_code, 200)
    
    def test_service_a_process(self):
        payload = {"data": "test"}
        response = requests.post(
            f"{self.base_urls['service_a']}/api/v1/process",
            json=payload
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['message'], 'Data processed successfully')
    
    def test_service_b_transaction(self):
        payload = {
            "id": "TXN123",
            "type": "payment",
            "amount": 100.50,
            "data": {}
        }
        response = requests.post(
            f"{self.base_urls['service_b']}/api/v1/transaction",
            json=payload
        )
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
