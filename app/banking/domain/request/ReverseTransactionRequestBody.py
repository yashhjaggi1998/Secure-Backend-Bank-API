from pydantic import BaseModel

class ReverseTransactionRequestBody(BaseModel):
    transaction_id: str