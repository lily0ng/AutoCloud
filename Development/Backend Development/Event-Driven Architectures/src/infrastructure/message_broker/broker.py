from abc import ABC, abstractmethod
from typing import Callable, Any
import pika
import json
import structlog
from core.events.event_bus import Event

logger = structlog.get_logger()

class MessageBroker(ABC):
    @abstractmethod
    def publish(self, routing_key: str, message: Any) -> None:
        pass

    @abstractmethod
    def subscribe(self, routing_key: str, callback: Callable) -> None:
        pass

class RabbitMQBroker(MessageBroker):
    def __init__(self, host: str = 'localhost', exchange: str = 'events'):
        self.host = host
        self.exchange = exchange
        self._connection = None
        self._channel = None
        self.setup()

    def setup(self) -> None:
        """Setup RabbitMQ connection and channel"""
        try:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host)
            )
            self._channel = self._connection.channel()
            self._channel.exchange_declare(
                exchange=self.exchange,
                exchange_type='topic'
            )
            logger.info("rabbitmq_setup_complete", host=self.host)
        except Exception as e:
            logger.error("rabbitmq_setup_failed", error=str(e))
            raise

    def publish(self, routing_key: str, message: Event) -> None:
        """Publish message to RabbitMQ"""
        try:
            self._channel.basic_publish(
                exchange=self.exchange,
                routing_key=routing_key,
                body=message.to_json()
            )
            logger.info("message_published", routing_key=routing_key)
        except Exception as e:
            logger.error("publish_failed", error=str(e))
            raise

    def subscribe(self, routing_key: str, callback: Callable) -> None:
        """Subscribe to messages with the given routing key"""
        try:
            result = self._channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue

            self._channel.queue_bind(
                exchange=self.exchange,
                queue=queue_name,
                routing_key=routing_key
            )

            def wrapped_callback(ch, method, properties, body):
                try:
                    event = Event.from_json(body.decode())
                    callback(event)
                    logger.info("message_processed", routing_key=routing_key)
                except Exception as e:
                    logger.error("message_processing_failed", error=str(e))

            self._channel.basic_consume(
                queue=queue_name,
                on_message_callback=wrapped_callback,
                auto_ack=True
            )
            
            logger.info("subscription_created", routing_key=routing_key)
        except Exception as e:
            logger.error("subscribe_failed", error=str(e))
            raise

    def start_consuming(self) -> None:
        """Start consuming messages"""
        try:
            self._channel.start_consuming()
        except Exception as e:
            logger.error("consuming_failed", error=str(e))
            raise

    def close(self) -> None:
        """Close the connection"""
        if self._connection:
            self._connection.close()
            logger.info("connection_closed")
