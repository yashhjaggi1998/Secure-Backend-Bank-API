from pydantic import BaseModel

class BankingDepositWithdrawRequestBody(BaseModel):
    amount: float
    account_id: int