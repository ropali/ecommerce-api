from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud import order as crud_order
from app.db.database import get_db
from app.schemas.order import Order as OrderSchema
from app.schemas.order import OrderCreate

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=List[OrderSchema])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all orders.

    Args:
        skip: Number of orders to skip (for pagination)
        limit: Maximum number of orders to return
        db: Database session

    Returns:
        List of orders
    """
    orders = crud_order.get_orders(db, skip=skip, limit=limit)
    return orders


@router.post("/", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Place a new order.

    Args:
        order: Validated order data
        db: Database session

    Returns:
        Created order

    """
    return crud_order.create_order(db=db, order=order)
