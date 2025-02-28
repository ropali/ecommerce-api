from sqlalchemy import Column, Float, Integer, String

from app.db.base import BaseModel


class Product(BaseModel):
    """
    Product database model with fields for ID, name, description, price, and stock.
    """

    __tablename__ = "products"

    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)

    def __str__(self):
        return f"{self.name} - {self.price} - {self.stock}"
