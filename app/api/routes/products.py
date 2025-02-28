from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import product as crud_product
from app.db.database import get_db
from app.exceptions.http_exceptions import ProductNotFoundException
from app.schemas.product import Product as ProductSchema
from app.schemas.product import ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductSchema])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all available products.

    Args:
        skip: Number of products to skip (for pagination)
        limit: Maximum number of products to return
        db: Database session

    Returns:
        List of products
    """
    products = crud_product.get_products(db, skip=skip, limit=limit)
    return products


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Add a new product to the platform.

    Args:
        product: Validated product data
        db: Database session

    Returns:
        Created product
    """
    return crud_product.create_product(db=db, product=product)


@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific product by ID.

    Args:
        product_id: ID of the product to retrieve
        db: Database session

    Returns:
        Product if found

    Raises:
        404: If product with given ID doesn't exist
    """
    try:
        return crud_product.get_product(db, product_id=product_id)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.put("/{product_id}", response_model=ProductSchema)
def update_product(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db)
):
    """
    Update a product.

    Args:
        product_id: ID of the product to update
        product: Validated update data
        db: Database session

    Returns:
        Updated product

    Raises:
        404: If product with given ID doesn't exist
    """
    try:
        return crud_product.update_product(db, product_id=product_id, product=product)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{product_id}", response_model=ProductSchema)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product.

    Args:
        product_id: ID of the product to delete
        db: Database session

    Returns:
        Deleted product

    Raises:
        404: If product with given ID doesn't exist
    """
    try:
        return crud_product.delete_product(db, product_id=product_id)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
