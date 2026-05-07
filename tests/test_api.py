from app.api.routes import app


def test_health_endpoint():
    tester = app.test_client()

    response = tester.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "Payment Monitoring API running"

def test_transaction_missing_amount_returns_400():
    tester = app.test_client()

    response = tester.post("/transaction", json={
        "user_id": 601,
        "merchant": "Nike",
        "status": "Approved",
        "country": "UK"
    })

    assert response.status_code == 400
    assert response.get_json()["error"] == "Missing required field: amount"

def test_transaction_invalid_amount_returns_400():
    tester = app.test_client()

    response = tester.post("/transaction", json={
        "user_id": 602,
        "merchant": "Apple",
        "amount": "expensive",
        "status": "Approved",
        "country": "UK"
    })

    assert response.status_code == 400
    assert response.get_json()["error"] == "Amount must be a number"