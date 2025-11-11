#!/usr/bin/env python3
"""Kafka Consumer Implementation"""

from kafka import KafkaConsumer
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageConsumer:
    def __init__(self, topic, group_id, bootstrap_servers=['localhost:9092']):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        logger.info(f"Kafka consumer subscribed to {topic}")
    
    def consume_messages(self, callback):
        try:
            for message in self.consumer:
                logger.info(f"Received message from partition {message.partition}")
                callback(message.value)
        except KeyboardInterrupt:
            logger.info("Consumer interrupted")
        finally:
            self.close()
    
    def close(self):
        self.consumer.close()
        logger.info("Kafka consumer closed")

if __name__ == "__main__":
    def process_message(msg):
        print(f"Processing: {msg}")
    
    consumer = MessageConsumer("events", "service-group")
    consumer.consume_messages(process_message)
