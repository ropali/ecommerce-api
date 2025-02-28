from typing import Any, Dict, List

from fastapi import Response, status

from app.models.product import Product


def create_order(client: Any, sample_products: List[Product]) -> Response:
    """Helper function to create an order."""
    order_data: Dict[str, Any] = {
        "items": [
            {"product_id": sample_products[0].id, "quantity": 2},
            {"product_id": sample_products[1].id, "quantity": 1},
        ]
    }
    return client.post("/api/v1/orders/", json=order_data)


def test_create_order(client: Any, sample_products: List[Any]) -> None:
    """Test creating a new order with valid data."""

    response = create_order(client, sample_products)
    assert response.status_code == status.HTTP_201_CREATED

    created_order: Dict[str, Any] = response.json()
    assert "id" in created_order
    assert created_order["status"] == "pending"
    assert len(created_order["items"]) == 2

    expected_total: float = sample_products[0].price * 2 + sample_products[1].price * 1
    assert created_order["total_price"] == expected_total

    for product in sample_products[:2]:
        product_response = client.get(f"/api/v1/products/{product.id}")
        expected_stock: int = product.stock - (
            2 if product == sample_products[0] else 1
        )
        assert product_response.json()["stock"] == expected_stock


def test_create_order_insufficient_stock(
    client: Any, sample_products: List[Any]
) -> None:
    """Test creating an order with insufficient stock."""
    order_data: Dict[str, Any] = {
        "items": [
            {
                "product_id": sample_products[0].id,
                "quantity": sample_products[0].stock + 1,
            }
        ]
    }
    response = client.post("/api/v1/orders/", json=order_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Insufficient stock" in response.json()["detail"]


def test_create_order_product_not_found(client: Any) -> None:
    """Test creating an order with a non-existent product."""
    order_data: Dict[str, Any] = {"items": [{"product_id": 999, "quantity": 1}]}
    response = client.post("/api/v1/orders/", json=order_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Product with ID 999 not found" in response.json()["detail"]


def test_duplicate_products_in_order(client: Any, sample_products: List[Any]) -> None:
    """Test creating an order with duplicate products."""
    order_data: Dict[str, Any] = {
        "items": [
            {"product_id": sample_products[0].id, "quantity": 1},
            {"product_id": sample_products[0].id, "quantity": 2},
        ]
    }
    response = client.post("/api/v1/orders/", json=order_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
