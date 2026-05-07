import csv
from app.database.db import SessionLocal
from app.database.models import Transaction
from app.fraud_detection.fraud_engine import detect_fraud


def calculate_metrics():
    db = SessionLocal()

    transactions = db.query(Transaction).all()

    total_transactions = len(transactions)
    approved_transactions = 0
    failed_transactions = 0
    suspicious_transactions = 0
    total_transaction_value = 0

    for transaction in transactions:
        total_transaction_value += transaction.amount

        if transaction.status.lower() == "approved":
            approved_transactions += 1

        if transaction.status.lower() == "failed":
            failed_transactions += 1

        transaction_data = {
            "user_id": transaction.user_id,
            "merchant": transaction.merchant,
            "amount": transaction.amount,
            "status": transaction.status,
            "country": transaction.country
        }

        fraud_result = detect_fraud(transaction_data)

        if fraud_result["is_suspicious"]:
            suspicious_transactions += 1

    db.close()

    if total_transactions == 0:
        average_transaction_value = 0
        failure_rate = 0
        fraud_alert_rate = 0
    else:
        average_transaction_value = total_transaction_value / total_transactions
        failure_rate = (failed_transactions / total_transactions) * 100
        fraud_alert_rate = (suspicious_transactions / total_transactions) * 100

    return {
        "total_transactions": total_transactions,
        "approved_transactions": approved_transactions,
        "failed_transactions": failed_transactions,
        "suspicious_transactions": suspicious_transactions,
        "total_transaction_value": round(total_transaction_value, 2),
        "average_transaction_value": round(average_transaction_value, 2),
        "failure_rate_percent": round(failure_rate, 2),
        "fraud_alert_rate_percent": round(fraud_alert_rate, 2)
    }


def export_metrics_report():
    metrics = calculate_metrics()

    file_path = "reports/transaction_metrics_report.csv"

    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Metric", "Value"])

        for key, value in metrics.items():
            writer.writerow([key, value])

    return file_path