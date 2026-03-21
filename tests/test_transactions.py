from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_transaction_success():
    payload = {
        "amount": 100.0,
        "type": "income",
        "category": "salary",
        "description": "March payroll",
        "date": "2026-03-14"
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["id"] == 1
    assert result["amount"] == 100.0
    assert result["type"] == "income"
    assert result["category"] == "salary"
    assert result["description"] == "March payroll"
    assert result["date"] == "2026-03-14"


def test_create_transaction_validation_errors():
    payload = {
        "amount": -5,
        "type": "invalid",
        "category": "",
        "description": "",
        "date": "wrong-date"
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 422
