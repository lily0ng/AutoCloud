from typing import List
from uuid import UUID
import structlog
from core.events.event_bus import Event, EventBus
from domain.models.order import Order, OrderItem

logger = structlog.get_logger()

class OrderService:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self._orders = {}  # In-memory storage for demonstration
        self._setup_event_handlers()

    def _setup_event_handlers(self) -> None:
        """Setup event handlers for order-related events"""
        self.event_bus.subscribe("ORDER_CREATED", self._handle_order_created)
        self.event_bus.subscribe("ORDER_PAYMENT_CONFIRMED", self._handle_payment_confirmed)
        self.event_bus.subscribe("ORDER_SHIPPED", self._handle_order_shipped)

    def create_order(self, customer_id: UUID, items: List[OrderItem]) -> Order:
        """Create a new order and publish ORDER_CREATED event"""
        order = Order.create(customer_id, items)
        self._orders[order.id] = order

        event = Event(
            event_type="ORDER_CREATED",
            data=order.to_dict()
        )
        self.event_bus.publish(event)
        logger.info("order_created", order_id=str(order.id))
        return order

    def _handle_order_created(self, event: Event) -> None:
        """Handle ORDER_CREATED event"""
        order_data = event.data
        logger.info("handling_order_created", order_id=order_data["id"])
        # Implement order creation logic
        # For example, validate inventory, reserve items, etc.

    def _handle_payment_confirmed(self, event: Event) -> None:
        """Handle ORDER_PAYMENT_CONFIRMED event"""
        order_id = UUID(event.data["order_id"])
        order = self._orders.get(order_id)
        
        if order:
            order.update_status("PAID")
            logger.info("payment_confirmed", order_id=str(order_id))
        else:
            logger.error("order_not_found", order_id=str(order_id))

    def _handle_order_shipped(self, event: Event) -> None:
        """Handle ORDER_SHIPPED event"""
        order_id = UUID(event.data["order_id"])
        order = self._orders.get(order_id)
        
        if order:
            order.update_status("SHIPPED")
            logger.info("order_shipped", order_id=str(order_id))
        else:
            logger.error("order_not_found", order_id=str(order_id))

    def get_order(self, order_id: UUID) -> Order:
        """Retrieve an order by ID"""
        return self._orders.get(order_id)
