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


def test_get_orders_empty(client: Any) -> None:
    """Test retrieving orders when none exist."""
    response = client.get("/api/v1/orders/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_orders(client: Any, sample_products: List[Any]) -> None:
    """Test retrieving all orders after creating some."""
    for _ in range(2):
        create_order(client, sample_products)

    response = client.get("/api/v1/orders/")
    assert response.status_code == status.HTTP_200_OK
    orders: List[Dict[str, Any]] = response.json()
    assert len(orders) == 2

    for order in orders:
        assert all(key in order for key in ["id", "status", "total_price", "items"])
        assert len(order["items"]) == 1


def test_get_order(client: Any, sample_products: List[Any]) -> None:
    """Test retrieving a specific order by ID."""
    response = create_order(client, sample_products)
    order_id: int = response.json()["id"]

    response = client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == status.HTTP_200_OK
    order: Dict[str, Any] = response.json()

    assert order["id"] == order_id
    assert order["status"] == "pending"
    assert len(order["items"]) == 2


def test_update_order_status(client: Any, sample_products: List[Any]) -> None:
    """Test updating an order's status."""
    response = create_order(client, sample_products)
    order_id: int = response.json()["id"]

    update_data: Dict[str, str] = {"status": "completed"}
    response = client.put(f"/api/v1/orders/{order_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK

    updated_order: Dict[str, Any] = response.json()
    assert updated_order["id"] == order_id
    assert updated_order["status"] == "completed"


def test_update_order_status_invalid(client: Any, sample_products: List[Any]) -> None:
    """Test updating an order with an invalid status."""
    response = create_order(client, sample_products)
    order_id: int = response.json()["id"]

    update_data: Dict[str, str] = {"status": "invalid_status"}
    response = client.put(f"/api/v1/orders/{order_id}", json=update_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_order_not_found(client: Any) -> None:
    """Test updating a non-existent order."""
    update_data: Dict[str, str] = {"status": "completed"}
    response = client.put("/api/v1/orders/999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Order with ID 999 not found" in response.json()["detail"]


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
