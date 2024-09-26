from pydantic import BaseModel
from typing import Optional

class AccountResponseBody(BaseModel):
    account_id: Optional[str] = None
    balance: Optional[float] = None
    account_name: Optional[str] = None
    error: Optional[str] = None