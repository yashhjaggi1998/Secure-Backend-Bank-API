from sqlalchemy import Column, Integer, String, DateTime, Float
from app.database import _dbBase

class Account(_dbBase):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key = True, nullable = False, index = True, unique = True)
    name = Column(String, nullable = False, index = True)
    balance = Column(Float, nullable = False, default = 0.0)
    created_at = Column(DateTime, nullable = False)
    deleted_at = Column(DateTime, nullable = True)