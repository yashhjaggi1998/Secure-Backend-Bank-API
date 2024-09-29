from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum
from app.banking.typings import TransactionType
from app.database import _dbBase

class Transaction(_dbBase):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key = True, nullable = False, index = True, unique = True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable = False)
    type = Column(String, nullable = False)
    amount = Column(Float, nullable = False)
    created_at = Column(DateTime, nullable = False)
    deleted_at = Column(DateTime, nullable = True)