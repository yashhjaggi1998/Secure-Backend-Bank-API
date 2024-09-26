from pydantic import BaseModel
from typing import Optional

class GetTransactionSummaryResponseBody(BaseModel):
    total_deposits: Optional[float] = None
    total_withdrawals: Optional[float] = None
    number_of_deposits: Optional[float] = None
    number_of_withdrawals: Optional[float] = None
    error: Optional[str] = None