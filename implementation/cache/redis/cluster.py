#!/usr/bin/env python3
"""Redis Cluster Manager"""

from rediscluster import RedisCluster
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisClusterManager:
    def __init__(self, startup_nodes):
        self.cluster = RedisCluster(
            startup_nodes=startup_nodes,
            decode_responses=True,
            skip_full_coverage_check=True
        )
        logger.info(f"Connected to Redis cluster with {len(startup_nodes)} nodes")
    
    def set_value(self, key, value, ttl=None):
        """Set a value in the cluster"""
        if ttl:
            self.cluster.setex(key, ttl, value)
        else:
            self.cluster.set(key, value)
        logger.debug(f"Set key: {key}")
    
    def get_value(self, key):
        """Get a value from the cluster"""
        return self.cluster.get(key)
    
    def delete_value(self, key):
        """Delete a value from the cluster"""
        self.cluster.delete(key)
        logger.debug(f"Deleted key: {key}")
    
    def get_cluster_info(self):
        """Get cluster information"""
        return {
            'cluster_nodes': len(self.cluster.cluster_nodes()),
            'cluster_slots': self.cluster.cluster_slots(),
        }
    
    def health_check(self):
        """Check cluster health"""
        try:
            self.cluster.ping()
            return True
        except Exception as e:
            logger.error(f"Cluster health check failed: {e}")
            return False

if __name__ == "__main__":
    nodes = [
        {"host": "127.0.0.1", "port": "7000"},
        {"host": "127.0.0.1", "port": "7001"},
        {"host": "127.0.0.1", "port": "7002"},
    ]
    
    cluster = RedisClusterManager(nodes)
    cluster.set_value("test_key", "test_value", ttl=60)
    print(f"Value: {cluster.get_value('test_key')}")
    print(f"Cluster Info: {cluster.get_cluster_info()}")
