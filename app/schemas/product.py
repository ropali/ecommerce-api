from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ProductBase(BaseModel):
    """
    Base schema for product attributes.
    """

    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    description: Optional[str] = Field(
        None, max_length=1000, description="Product description"
    )
    price: float = Field(..., gt=0, description="Product price")
    stock: int = Field(..., ge=0, description="Available stock quantity")

    @field_validator("price")
    def price_must_be_positive(cls, v):  # noqa: N805
        """Validate that price is positive and has at most 2 decimal places."""
        if v <= 0:
            raise ValueError("Price must be positive")
        # Check decimal places
        str_v = str(v)
        if "." in str_v and len(str_v.split(".")[1]) > 2:
            raise ValueError("Price must have at most 2 decimal places")
        return v


class ProductCreate(ProductBase):
    """
    Schema for creating new products.
    """

    pass


class ProductUpdate(BaseModel):
    """
    Schema for updating products, all fields are optional.
    """

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)

    @field_validator("price")
    def price_must_be_positive(cls, v):  # noqa: N805
        """Validate that price is positive and has at most 2 decimal places."""
        if v is not None:
            if v <= 0:
                raise ValueError("Price must be positive")
            # Check decimal places
            str_v = str(v)
            if "." in str_v and len(str_v.split(".")[1]) > 2:
                raise ValueError("Price must have at most 2 decimal places")
        return v


class ProductInDB(ProductBase):
    """
    Schema for products as stored in database, including ID and timestamps.
    """

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Product(ProductInDB):
    """
    Schema for product responses, inherits all fields from ProductInDB.
    """

    pass
