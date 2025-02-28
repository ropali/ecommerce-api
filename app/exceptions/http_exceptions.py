from fastapi import HTTPException, status


class InsufficientStockException(HTTPException):
    """
    Exception raised when there is insufficient stock for a product.
    This happens when a customer tries to order more than what's available.
    """

    def __init__(
        self, product_id: int, requested_quantity: int, available_quantity: int
    ):
        self.product_id = product_id
        self.requested_quantity = requested_quantity
        self.available_quantity = available_quantity

        detail = (
            f"Insufficient stock for product ID {product_id}. "
            f"Requested: {requested_quantity}, Available: {available_quantity}"
        )

        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ProductNotFoundException(HTTPException):
    """
    Exception raised when a product is not found in the database.
    This occurs when trying to access a product with an ID that doesn't exist.
    """

    def __init__(self, product_id: int):
        self.product_id = product_id

        detail = f"Product with ID {product_id} not found"

        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class OrderNotFoundException(HTTPException):
    """
    Exception raised when an order is not found in the database.
    This occurs when trying to access an order with an ID that doesn't exist.
    """

    def __init__(self, order_id: int):
        self.order_id = order_id

        detail = f"Order with ID {order_id} not found"

        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InvalidOrderDataException(HTTPException):
    """
    Exception raised when order data is invalid.
    This could happen for various reasons, such as trying to order out-of-stock products
    or providing malformed data.
    """

    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
