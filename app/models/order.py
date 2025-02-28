import enum

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import BaseModel


class OrderStatus(str, enum.Enum):
    """
    Enumeration for possible order statuses.
    """

    PENDING = "pending"
    COMPLETED = "completed"


class Order(BaseModel):
    """
    Order database model with fields for ID, status, and total price.
    """

    __tablename__ = "orders"

    status = Column(String, default=OrderStatus.PENDING.value)
    total_price = Column(Float, nullable=False)

    # Relationship with OrderItem
    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(BaseModel):
    """
    Order item model to represent many-to-many relationship between orders and products
    with additional quantity field.
    """

    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")
