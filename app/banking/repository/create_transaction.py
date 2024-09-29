from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from ...db_connector import get_db
from ..domain.models.transaction_model import Transaction

async def create_transaction(account_id: int, transaction_type: str, amount: int, db: AsyncSession = Depends(get_db)):
    transaction = Transaction(
        account_id = account_id,
        type = transaction_type,
        amount = amount,
        created_at = datetime.now()
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction