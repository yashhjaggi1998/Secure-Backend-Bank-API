from typing import List, Tuple, Union
from enum import Enum

any = Union[str, float, int, bool]

CreateAccountParams = Tuple[str, any]

UpdateAccountFieldParams = List[Tuple[str, any]]

UpdateTransactionFieldParams = List[Tuple[str, any]]

class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"