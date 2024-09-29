from sqlalchemy.ext.asyncio import AsyncSession
from app.banking.repository.get_transaction import get_transaction_by_id
from app.banking.typings import UpdateAccountFieldParams

async def update_transaction_fields(transaction_id: int, field_params: UpdateAccountFieldParams, db: AsyncSession):
    transaction = await get_transaction_by_id(transaction_id, db)
    if not transaction:
        raise Exception("Transaction not found")
    
    for field, value in field_params:
        if field not in ["type", "amount", "account_id"]:
            raise Exception("Invalid field to update in transaction table")    
        setattr(transaction, field, value)

    await db.commit()
    await db.refresh(transaction)
    return transaction