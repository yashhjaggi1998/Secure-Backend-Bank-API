from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Transaction(BaseModel):
    id: int
    account_id: int
    type: str
    amount: float
    created_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True