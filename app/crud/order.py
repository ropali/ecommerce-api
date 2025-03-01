from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.crud.product import get_product, update_product_stock
from app.exceptions.http_exceptions import InsufficientStockException, InvalidOrderDataException
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import OrderCreate


def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
    """
    Retrieve a list of orders with optional pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Order objects
    """
    return db.query(Order).offset(skip).limit(limit).all()


def create_order(db: Session, order: OrderCreate) -> Order:
    """
    Create a new order after validating product availability.

    Args:
        db: Database session
        order: Validated order data

    Returns:
        The created Order object

    Raises:
        ProductNotFoundException: If any product in the order doesn't exist
        InsufficientStockException: If any product doesn't have enough stock
        InvalidOrderDataException: If order data is invalid
    """
    # Validate products and stock availability
    product_data = []
    total_price = 0.0

    # Check each product in the order
    for item in order.items:
        product = get_product(db, item.product_id)

        # Check if there's enough stock
        if product.stock < item.quantity:
            raise InsufficientStockException(
                product_id=product.id,
                requested_quantity=item.quantity,
                available_quantity=product.stock,
            )

        # Calculate price for this line item
        item_price = product.price * item.quantity
        total_price += item_price

        # Store product data for later
        product_data.append((product, item.quantity, product.price))

    # Start a transaction
    try:

        # Create order
        db_order = Order(total_price=total_price, status=OrderStatus.PENDING.value)
        db.add(db_order)
        db.flush()  # Get the order ID before committing

        # Create order items
        for product, quantity, price in product_data:
            order_item = OrderItem(
                order_id=db_order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=price,
            )
            db.add(order_item)

            # Update product stock
            update_product_stock(db, product.id, -quantity)

        # Commit the transaction
        db.commit()
        db.refresh(db_order)
        return db_order

    except SQLAlchemyError as e:
        db.rollback()
        raise InvalidOrderDataException(str(e))
