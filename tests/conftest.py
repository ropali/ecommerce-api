from typing import List

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app
from app.models.product import Product

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_db():
    """
    Create a fresh database for each test function.
    """
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create the tables
    Base.metadata.create_all(bind=engine)

    # Create a new session for each test
    db = local_session()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after the test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """
    Create a test client using the test database.
    """

    # Override the get_db dependency to use the test database
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client


@pytest.fixture
def sample_products(test_db) -> List[Product]:
    """
    Create sample products for testing.
    """
    products = [
        Product(
            name="Test Product 1",
            description="Description for test product 1",
            price=19.99,
            stock=10,
        ),
        Product(
            name="Test Product 2",
            description="Description for test product 2",
            price=29.99,
            stock=5,
        ),
        Product(
            name="Test Product 3",
            description="Description for test product 3",
            price=39.99,
            stock=0,
        ),
    ]

    test_db.add_all(products)
    test_db.commit()

    for product in products:
        test_db.refresh(product)

    return products
