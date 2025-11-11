from typing import Dict, List, Callable, Any
from abc import ABC, abstractmethod
import json
import structlog

logger = structlog.get_logger()

class Event:
    def __init__(self, event_type: str, data: Dict[str, Any], version: str = "1.0"):
        self.event_type = event_type
        self.data = data
        self.version = version

    def to_json(self) -> str:
        return json.dumps({
            "event_type": self.event_type,
            "data": self.data,
            "version": self.version
        })

    @classmethod
    def from_json(cls, json_str: str) -> 'Event':
        event_dict = json.loads(json_str)
        return cls(
            event_type=event_dict["event_type"],
            data=event_dict["data"],
            version=event_dict["version"]
        )

class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._middleware: List[Callable] = []
        
    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe a handler to a specific event type"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        logger.info("handler_subscribed", event_type=event_type, handler=handler.__name__)

    def publish(self, event: Event) -> None:
        """Publish an event to all subscribed handlers"""
        event_handlers = self._handlers.get(event.event_type, [])
        
        # Apply middleware
        for middleware in self._middleware:
            event = middleware(event)
            
        for handler in event_handlers:
            try:
                handler(event)
                logger.info(
                    "event_handled",
                    event_type=event.event_type,
                    handler=handler.__name__
                )
            except Exception as e:
                logger.error(
                    "event_handling_failed",
                    event_type=event.event_type,
                    handler=handler.__name__,
                    error=str(e)
                )

    def add_middleware(self, middleware: Callable) -> None:
        """Add middleware to process events before they reach handlers"""
        self._middleware.append(middleware)

class EventStore:
    def __init__(self):
        self._events: List[Event] = []

    def append(self, event: Event) -> None:
        """Store an event in the event store"""
        self._events.append(event)
        logger.info("event_stored", event_type=event.event_type)

    def get_events(self, event_type: str = None) -> List[Event]:
        """Retrieve events, optionally filtered by type"""
        if event_type:
            return [e for e in self._events if e.event_type == event_type]
        return self._events.copy()

class EventProducer(ABC):
    @abstractmethod
    def produce_event(self, event: Event) -> None:
        pass

class EventConsumer(ABC):
    @abstractmethod
    def consume_event(self, event: Event) -> None:
        pass
