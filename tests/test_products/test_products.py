from typing import Dict, List

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.models.product import Product


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


def test_get_products_empty(client: TestClient) -> None:
    """Test retrieving products when none exist."""
    response = client.get("/api/v1/products/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_products(client: TestClient, sample_products: List[Dict]) -> None:
    """Test retrieving all products."""
    response = client.get("/api/v1/products/")
    assert response.status_code == status.HTTP_200_OK
    products = response.json()
    assert len(products) == 3

    for product in products:
        assert "id" in product
        assert "name" in product
        assert "description" in product
        assert "price" in product
        assert "stock" in product


def test_create_product(client: TestClient) -> None:
    """Test creating a new product."""
    product_data: Dict[str, str | float | int] = {
        "name": "New Test Product",
        "description": "Description for new test product",
        "price": 49.99,
        "stock": 15,
    }

    response = client.post("/api/v1/products/", json=product_data)
    assert response.status_code == status.HTTP_201_CREATED

    created_product = response.json()
    assert created_product["name"] == product_data["name"]
    assert created_product["description"] == product_data["description"]
    assert created_product["price"] == product_data["price"]
    assert created_product["stock"] == product_data["stock"]
    assert "id" in created_product


def test_create_product_invalid_data(client: TestClient) -> None:
    """Test creating a product with invalid data."""
    product_data: Dict[str, str | float | int] = {
        "description": "Description for new test product",
        "price": 49.99,
        "stock": 15,
    }
    response = client.post("/api/v1/products/", json=product_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    product_data = {
        "name": "New Test Product",
        "description": "Description for new test product",
        "price": -10.0,
        "stock": 15,
    }
    response = client.post("/api/v1/products/", json=product_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    product_data = {
        "name": "New Test Product",
        "description": "Description for new test product",
        "price": 49.99,
        "stock": -5,
    }
    response = client.post("/api/v1/products/", json=product_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_product(client: TestClient, sample_products: List[Dict]) -> None:
    """Test retrieving a specific product by ID."""
    product_id: int = sample_products[0].id

    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == status.HTTP_200_OK

    product = response.json()
    assert product["id"] == product_id
    assert product["name"] == sample_products[0]["name"]


def test_get_product_not_found(client: TestClient) -> None:
    """Test retrieving a non-existent product."""
    response = client.get("/api/v1/products/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Product with ID 999 not found"


def test_update_product(client: TestClient, sample_products: List[Dict]) -> None:
    """Test updating a product."""
    product_id: int = sample_products[0].id

    update_data: Dict[str, str | float] = {
        "name": "Updated Product Name",
        "price": 59.99,
    }

    response = client.put(f"/api/v1/products/{product_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK

    updated_product = response.json()
    assert updated_product["id"] == product_id
    assert updated_product["name"] == update_data["name"]
    assert updated_product["price"] == update_data["price"]
    assert updated_product["description"] == sample_products[0]["description"]
    assert updated_product["stock"] == sample_products[0]["stock"]


def test_update_product_not_found(client: TestClient) -> None:
    """Test updating a non-existent product."""
    update_data: Dict[str, str | float] = {
        "name": "Updated Product Name",
        "price": 59.99,
    }
    response = client.put("/api/v1/products/999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Product with ID 999 not found"


def test_delete_product(client: TestClient, sample_products: List[Dict]) -> None:
    """Test deleting a product."""
    product_id: int = sample_products[0].id

    response = client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == status.HTTP_200_OK

    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_product_not_found(client: TestClient) -> None:
    """Test deleting a non-existent product."""
    response = client.delete("/api/v1/products/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Product with ID 999 not found"
