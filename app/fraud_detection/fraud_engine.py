def detect_fraud(transaction_data):
    alerts = []

    amount = transaction_data["amount"]
    status = transaction_data["status"]
    country = transaction_data["country"]

    if amount > 5000:
        alerts.append("High-value transaction flagged")

    if status.lower() == "failed":
        alerts.append("Failed transaction flagged")

    if country.upper() not in ["UK", "GB", "UNITED KINGDOM"]:
        alerts.append("International transaction flagged")

    is_suspicious = len(alerts) > 0

    return {
        "is_suspicious": is_suspicious,
        "alerts": alerts
    }