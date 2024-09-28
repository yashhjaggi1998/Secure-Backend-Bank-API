from pydantic import BaseModel

class CreateAccountRequestBody(BaseModel):
    name: str
    balance: float