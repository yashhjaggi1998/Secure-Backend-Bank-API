from pydantic import BaseModel
from typing import Optional

class GetValidateAccountIdResponse(BaseModel):
    accountId: Optional[str] = None
    accountBalance: Optional[float] = None
    balanceFromTransactions: Optional[float] = None
    isValid: Optional[bool] = None
    error: Optional[str] = None