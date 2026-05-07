from app.database.db import SessionLocal
from app.database.models import Transaction

def create_transaction(user_id, merchant, amount, status, country):

    db = SessionLocal()

    transaction = Transaction(
        user_id=user_id,
        merchant=merchant,
        amount=amount,
        status=status,
        country=country
    )

    db.add(transaction)
    db.commit()

    db.close()

    return transaction