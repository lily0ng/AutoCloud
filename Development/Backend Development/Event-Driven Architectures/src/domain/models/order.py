from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

@dataclass
class OrderItem:
    product_id: UUID
    quantity: int
    price: float

@dataclass
class Order:
    id: UUID
    customer_id: UUID
    items: List[OrderItem]
    total_amount: float
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    @classmethod
    def create(cls, customer_id: UUID, items: List[OrderItem]) -> 'Order':
        total_amount = sum(item.price * item.quantity for item in items)
        return cls(
            id=uuid4(),
            customer_id=customer_id,
            items=items,
            total_amount=total_amount,
            status="PENDING",
            created_at=datetime.utcnow()
        )

    def update_status(self, new_status: str) -> None:
        self.status = new_status
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "customer_id": str(self.customer_id),
            "items": [
                {
                    "product_id": str(item.product_id),
                    "quantity": item.quantity,
                    "price": item.price
                }
                for item in self.items
            ],
            "total_amount": self.total_amount,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
