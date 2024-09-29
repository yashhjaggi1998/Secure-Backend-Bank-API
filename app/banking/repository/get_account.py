from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..domain.models.account_model import Account

async def get_account(account_id: int, db: AsyncSession) -> Account:
    result = await db.execute(select(Account).where(
        Account.id == account_id,
        Account.deleted_at.is_(None)    
    ))
    account = result.scalars().first()
    return account