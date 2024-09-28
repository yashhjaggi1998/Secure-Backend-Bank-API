from pydantic import BaseModel
from typing import Optional

class UpdateAccountRequestBody(BaseModel):
    account_id: int
    name: Optional[str] = None
    balance: Optional[float] = None