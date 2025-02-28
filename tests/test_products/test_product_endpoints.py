from typing import Dict, List

from fastapi import status
from fastapi.testclient import TestClient


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
