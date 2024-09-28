from datetime import datetime

from fastapi import Depends

from ...db_connector import get_db
from ..domain.models.account_model import Account
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def create_account(account_name: str, balance: int, db: AsyncSession = Depends(get_db)):
    db_account = await db.execute(select(Account.id).order_by(Account.id.desc()).limit(1))
    account_id = db_account.fetchone()[0] + 1

    account = Account(
        id = account_id, 
        name = account_name, 
        balance = balance, 
        created_at = datetime.now()
    )
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account