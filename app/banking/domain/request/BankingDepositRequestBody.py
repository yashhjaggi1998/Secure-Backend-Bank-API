from pydantic import BaseModel

class BankingDepositRequestBody(BaseModel):
    amount: float
    account_id: str