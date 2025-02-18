import os
import sys

# Agregar la carpeta raíz al path de Python
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../fastapi"))
)

from main import app  # Ahora debería poder importarse correctamente

from fastapi.testclient import TestClient

client = TestClient(app)


def test_add_purchase():
    response = client.post(
        "/purchase/",
        json={
            "customer_name": "John Doe",
            "country": "USA",
            "purchase_date": "2024-02-18",
            "amount": 100.0,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["country"] == "USA"
    assert data["amount"] == 100.0


def test_get_purchases():
    response = client.get("/purchases/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_kpis():
    response = client.get("/purchases/kpis/")
    assert response.status_code == 200
    assert "average_purchase_per_client" in response.json()
    assert "clients_per_country" in response.json()
