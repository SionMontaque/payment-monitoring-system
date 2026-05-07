from flask import Flask, jsonify, request
from app.database.db import SessionLocal
from app.database.models import Transaction
from app.services.transaction_service import create_transaction
from app.fraud_detection.fraud_engine import detect_fraud
from app.monitoring.metrics_service import calculate_metrics, export_metrics_report
from app.utils.logger import logger


app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "Payment Monitoring API running"
    })


@app.route("/transaction", methods=["POST"])
def add_transaction():
    try:
        data = request.get_json()

        required_fields = ["user_id", "merchant", "amount", "status", "country"]

        for field in required_fields:
            if field not in data:
                logger.warning(f"Transaction rejected: missing field '{field}'")

                return jsonify({
                    "error": f"Missing required field: {field}"
                }), 400

        if not isinstance(data["amount"], (int, float)):
            logger.warning("Transaction rejected: amount must be numeric")

            return jsonify({
                "error": "Amount must be a number"
            }), 400

        fraud_result = detect_fraud(data)

        transaction = create_transaction(
            user_id=data["user_id"],
            merchant=data["merchant"],
            amount=data["amount"],
            status=data["status"],
            country=data["country"]
        )

        logger.info(
            f"Transaction created: user_id={data['user_id']}, "
            f"merchant={data['merchant']}, amount={data['amount']}, "
            f"suspicious={fraud_result['is_suspicious']}"
        )

        return jsonify({
            "message": "Transaction created successfully",
            "fraud_check": fraud_result
        }), 201

    except Exception as error:
        logger.error(f"Unexpected transaction error: {str(error)}")

        return jsonify({
            "error": "An unexpected error occurred while processing the transaction"
        }), 500


@app.route("/transactions", methods=["GET"])
def get_transactions():
    db = SessionLocal()

    transactions = db.query(Transaction).all()

    results = []

    for transaction in transactions:
        results.append({
            "id": transaction.id,
            "user_id": transaction.user_id,
            "merchant": transaction.merchant,
            "amount": transaction.amount,
            "status": transaction.status,
            "country": transaction.country
        })

    db.close()

    return jsonify(results)


@app.route("/fraud-alerts", methods=["GET"])
def get_fraud_alerts():
    db = SessionLocal()

    transactions = db.query(Transaction).all()

    alerts = []

    for transaction in transactions:
        transaction_data = {
            "user_id": transaction.user_id,
            "merchant": transaction.merchant,
            "amount": transaction.amount,
            "status": transaction.status,
            "country": transaction.country
        }

        fraud_result = detect_fraud(transaction_data)

        if fraud_result["is_suspicious"]:
            alerts.append({
                "transaction_id": transaction.id,
                "user_id": transaction.user_id,
                "merchant": transaction.merchant,
                "amount": transaction.amount,
                "status": transaction.status,
                "country": transaction.country,
                "alerts": fraud_result["alerts"]
            })

    db.close()

    logger.info(f"Fraud alerts retrieved: count={len(alerts)}")

    return jsonify(alerts)


@app.route("/metrics", methods=["GET"])
def get_metrics():
    try:
        metrics = calculate_metrics()

        logger.info("System metrics retrieved successfully")

        return jsonify(metrics), 200

    except Exception as error:
        logger.error(f"Metrics retrieval failed: {str(error)}")

        return jsonify({
            "error": "Unable to retrieve system metrics"
        }), 500


@app.route("/export-report", methods=["GET"])
def export_report():
    try:
        file_path = export_metrics_report()

        logger.info(f"Metrics report exported: {file_path}")

        return jsonify({
            "message": "Metrics report exported successfully",
            "file_path": file_path
        }), 200

    except Exception as error:
        logger.error(f"Report export failed: {str(error)}")

        return jsonify({
            "error": "Unable to export metrics report"
        }), 500

