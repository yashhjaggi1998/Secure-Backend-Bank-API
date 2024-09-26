from pydantic import BaseModel
from typing import Optional, List, Literal

class Transaction(BaseModel):
    account_id: Optional[str] = None
    transaction_id: Optional[str] = None
    transaction_type: Optional[Literal["deposit", "withdrawal", None]] = None
    amount: Optional[float] = None

class GetAllTransactionsResponseBody(BaseModel):
    transactions: Optional[List[Transaction]] = None
    error: Optional[str] = None