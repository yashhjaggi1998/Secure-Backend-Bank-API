from pydantic import BaseModel
from typing import Optional

# returns the account balance or an error message. Either are optional
class GetAccountBalanceResponseBody(BaseModel):
    balance: Optional[float] = None
    error: Optional[str] = None