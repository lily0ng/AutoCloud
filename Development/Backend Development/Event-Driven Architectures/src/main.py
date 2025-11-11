import asyncio
import uuid
from core.events.event_bus import EventBus, Event
from infrastructure.message_broker.broker import RabbitMQBroker
from domain.services.order_service import OrderService
from domain.models.order import OrderItem
import structlog

logger = structlog.get_logger()

async def main():
    # Initialize the event bus
    event_bus = EventBus()
    
    # Initialize the message broker
    broker = RabbitMQBroker(host='localhost')
    
    # Initialize the order service
    order_service = OrderService(event_bus)

    # Create a sample order
    customer_id = uuid.uuid4()
    items = [
        OrderItem(
            product_id=uuid.uuid4(),
            quantity=2,
            price=29.99
        ),
        OrderItem(
            product_id=uuid.uuid4(),
            quantity=1,
            price=49.99
        )
    ]

    # Create an order
    order = order_service.create_order(customer_id, items)
    logger.info("order_created", order_id=str(order.id))

    # Simulate payment confirmation
    payment_confirmed_event = Event(
        event_type="ORDER_PAYMENT_CONFIRMED",
        data={"order_id": str(order.id)}
    )
    event_bus.publish(payment_confirmed_event)

    # Simulate order shipment
    shipping_event = Event(
        event_type="ORDER_SHIPPED",
        data={"order_id": str(order.id)}
    )
    event_bus.publish(shipping_event)

    # Retrieve and display the final order state
    final_order = order_service.get_order(order.id)
    logger.info(
        "final_order_state",
        order_id=str(final_order.id),
        status=final_order.status
    )

if __name__ == "__main__":
    asyncio.run(main())
