from datetime import datetime
from app.banking.repository.get_account import get_account
from sqlalchemy.ext.asyncio import AsyncSession


async def soft_delete_account(account_id: int, db: AsyncSession):
    account = await get_account(account_id, db) # handles the case where account_id is not found
    if not account:
        raise Exception("Account not found")
    
    account.deleted_at = datetime.now()
    await db.commit()
    return account