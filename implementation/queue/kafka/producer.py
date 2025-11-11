#!/usr/bin/env python3
"""Kafka Producer Implementation"""

from kafka import KafkaProducer
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageProducer:
    def __init__(self, bootstrap_servers=['localhost:9092']):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
        logger.info(f"Kafka producer connected to {bootstrap_servers}")
    
    def send_message(self, topic: str, message: dict, key: str = None):
        message['timestamp'] = datetime.now().isoformat()
        future = self.producer.send(topic, value=message, key=key)
        try:
            record_metadata = future.get(timeout=10)
            logger.info(f"Message sent to {record_metadata.topic} partition {record_metadata.partition}")
            return True
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    def close(self):
        self.producer.close()
        logger.info("Kafka producer closed")

if __name__ == "__main__":
    producer = MessageProducer()
    producer.send_message("events", {"event": "user_login", "user_id": 123})
    producer.close()
