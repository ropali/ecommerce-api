from typing import List

from sqlalchemy.orm import Session

from app.exceptions.http_exceptions import ProductNotFoundException
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    """
    Retrieve a list of products with optional pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Product objects
    """
    return db.query(Product).offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int) -> Product:
    """
    Retrieve a single product by ID.

    Args:
        db: Database session
        product_id: ID of the product to retrieve

    Returns:
        Product object if found

    Raises:
        ProductNotFoundException: If product with given ID doesn't exist
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise ProductNotFoundException(product_id=product_id)
    return product


def create_product(db: Session, product: ProductCreate) -> Product:
    """
    Create a new product.

    Args:
        db: Database session
        product: Validated product data

    Returns:
        The created Product object
    """
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: ProductUpdate) -> Product:
    """
    Update an existing product.

    Args:
        db: Database session
        product_id: ID of the product to update
        product: Validated update data

    Returns:
        The updated Product object

    Raises:
        ProductNotFoundException: If product with given ID doesn't exist
    """
    db_product = get_product(db, product_id)

    # Only update fields that are provided
    update_data = product.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> Product:
    """
    Delete a product.

    Args:
        db: Database session
        product_id: ID of the product to delete

    Returns:
        The deleted Product object

    Raises:
        ProductNotFoundException: If product with given ID doesn't exist
    """
    db_product = get_product(db, product_id)
    db.delete(db_product)
    db.commit()
    return db_product


def update_product_stock(db: Session, product_id: int, quantity_change: int) -> Product:
    """
    Update the stock of a product by a given amount (positive or negative).

    Args:
        db: Database session
        product_id: ID of the product to update
        quantity_change: Amount to change stock by (negative to decrease)

    Returns:
        The updated Product object

    Raises:
        ProductNotFoundException: If product with given ID doesn't exist
        ValueError: If stock would go negative
    """
    db_product = get_product(db, product_id)

    new_stock = db_product.stock + quantity_change

    if new_stock < 0:
        raise ValueError(
            f"Cannot reduce stock below zero (product_id={product_id}, "
            f"current={db_product.stock}, change={quantity_change})"
        )

    db_product.stock = new_stock
    db.commit()
    db.refresh(db_product)
    return db_product
