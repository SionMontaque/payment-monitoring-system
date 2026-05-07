from sqlalchemy import Column, Integer, String, Float
from app.database.db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    merchant = Column(String)
    amount = Column(Float)
    status = Column(String)
    country = Column(String)