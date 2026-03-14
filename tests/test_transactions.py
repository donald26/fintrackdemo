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
    json_data = response.json()
    assert json_data["id"] == 1
    assert json_data["amount"] == 100.0
    assert json_data["type"] == "income"
    assert json_data["category"] == "salary"
    assert json_data["description"] == "March payroll"
    assert json_data["date"] == "2026-03-14"


def test_create_transaction_validation_errors():
    payload = {
        "amount": -10,
        "type": "other",
        "category": "",
        "description": "",
        "date": "not-a-date"
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 422
