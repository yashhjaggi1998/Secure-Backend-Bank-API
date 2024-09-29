from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    error_code: int
    message: str