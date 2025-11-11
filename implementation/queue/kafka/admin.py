#!/usr/bin/env python3
"""Kafka Admin Operations"""

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KafkaAdmin:
    def __init__(self, bootstrap_servers=['localhost:9092']):
        self.admin = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers,
            client_id='kafka-admin'
        )
        logger.info(f"Connected to Kafka at {bootstrap_servers}")
    
    def create_topic(self, topic_name, num_partitions=3, replication_factor=1):
        """Create a new topic"""
        topic = NewTopic(
            name=topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor
        )
        
        try:
            self.admin.create_topics([topic])
            logger.info(f"Topic '{topic_name}' created successfully")
            return True
        except TopicAlreadyExistsError:
            logger.warning(f"Topic '{topic_name}' already exists")
            return False
    
    def delete_topic(self, topic_name):
        """Delete a topic"""
        try:
            self.admin.delete_topics([topic_name])
            logger.info(f"Topic '{topic_name}' deleted successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to delete topic: {e}")
            return False
    
    def list_topics(self):
        """List all topics"""
        topics = self.admin.list_topics()
        return topics
    
    def describe_topic(self, topic_name):
        """Get topic details"""
        topics = self.admin.describe_topics([topic_name])
        return topics
    
    def close(self):
        """Close admin client"""
        self.admin.close()
        logger.info("Admin client closed")

if __name__ == "__main__":
    admin = KafkaAdmin()
    
    admin.create_topic("events", num_partitions=3)
    admin.create_topic("logs", num_partitions=5)
    
    topics = admin.list_topics()
    print(f"Topics: {topics}")
    
    admin.close()
