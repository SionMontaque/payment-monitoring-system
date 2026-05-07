from app.fraud_detection.fraud_engine import detect_fraud


def test_normal_transaction_not_flagged():
    transaction_data = {
        "user_id": 501,
        "merchant": "Tesco",
        "amount": 25.50,
        "status": "Approved",
        "country": "UK"
    }

    result = detect_fraud(transaction_data)

    assert result["is_suspicious"] is False
    assert result["alerts"] == []

def test_high_value_transaction_flagged():
    transaction_data = {
        "user_id": 502,
        "merchant": "Luxury Watches Ltd",
        "amount": 7500,
        "status": "Approved",
        "country": "UK"
    }

    result = detect_fraud(transaction_data)

    assert result["is_suspicious"] is True
    assert "High-value transaction flagged" in result["alerts"]   

def test_failed_transaction_flagged():
    transaction_data = {
        "user_id": 503,
        "merchant": "Nike",
        "amount": 120,
        "status": "Failed",
        "country": "UK"
    }

    result = detect_fraud(transaction_data)

    assert result["is_suspicious"] is True
    assert "Failed transaction flagged" in result["alerts"]

def test_international_transaction_flagged():
    transaction_data = {
        "user_id": 504,
        "merchant": "US Electronics",
        "amount": 800,
        "status": "Approved",
        "country": "USA"
    }

    result = detect_fraud(transaction_data)

    assert result["is_suspicious"] is True
    assert "International transaction flagged" in result["alerts"]   


def test_multiple_fraud_rules_triggered():
    transaction_data = {
        "user_id": 505,
        "merchant": "Crypto Exchange",
        "amount": 9000,
        "status": "Failed",
        "country": "USA"
    }

    result = detect_fraud(transaction_data)

    assert result["is_suspicious"] is True
    assert len(result["alerts"]) == 3