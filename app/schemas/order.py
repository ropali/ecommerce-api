from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    """
    Schema for creating order items.
    """

    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity of product")


class OrderItemInDB(OrderItemCreate):
    """
    Schema for order items as stored in database, including ID and unit price.
    """

    id: int
    unit_price: float

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    """
    Schema for creating new orders.
    """

    items: List[OrderItemCreate] = Field(
        ..., min_items=1, description="List of order items"
    )

    @field_validator("items")
    def items_must_be_unique(cls, v):  # noqa: N805
        """Validate that each product appears only once in the order."""
        product_ids = [item.product_id for item in v]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError("Duplicate products in order. Use quantity field instead.")
        return v


class OrderUpdate(BaseModel):
    """
    Schema for updating orders, allowing status updates.
    """

    status: Optional[OrderStatus] = None


class OrderInDB(BaseModel):
    """
    Schema for orders as stored in database, including all fields.
    """

    id: int
    status: str
    total_price: float
    items: List[OrderItemInDB]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Order(OrderInDB):
    """
    Schema for order responses, inherits all fields from OrderInDB.
    """

    pass
