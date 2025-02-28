from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud import product as crud_product
from app.db.database import get_db
from app.schemas.product import Product as ProductSchema
from app.schemas.product import ProductCreate

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
