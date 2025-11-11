#!/usr/bin/env python3
"""Unit tests for cache module"""

import unittest
from unittest.mock import Mock, patch
import sys
sys.path.insert(0, '../../cache/redis')
from client import RedisCache

class TestRedisCache(unittest.TestCase):
    
    @patch('redis.Redis')
    def setUp(self, mock_redis):
        self.cache = RedisCache()
        self.mock_client = self.cache.client
    
    def test_set_value(self):
        self.cache.set('test_key', 'test_value', ttl=60)
        self.mock_client.setex.assert_called_once()
    
    def test_get_value(self):
        self.mock_client.get.return_value = b'test_value'
        result = self.cache.get('test_key')
        self.assertIsNotNone(result)
    
    def test_delete_value(self):
        self.cache.delete('test_key')
        self.mock_client.delete.assert_called_once_with('test_key')
    
    def test_exists(self):
        self.mock_client.exists.return_value = 1
        result = self.cache.exists('test_key')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
