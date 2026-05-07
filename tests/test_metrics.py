from app.monitoring.metrics_service import calculate_metrics


def test_calculate_metrics_returns_expected_keys():
    metrics = calculate_metrics()

    expected_keys = [
        "total_transactions",
        "approved_transactions",
        "failed_transactions",
        "suspicious_transactions",
        "total_transaction_value",
        "average_transaction_value",
        "failure_rate_percent",
        "fraud_alert_rate_percent"
    ]

    for key in expected_keys:
        assert key in metrics