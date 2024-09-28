from app.banking.repository.get_account import get_account
from sqlalchemy.ext.asyncio import AsyncSession
from app.banking.typings import UpdateAccountFieldParams


async def update_account_fields(account_id: int, field_params: UpdateAccountFieldParams, db: AsyncSession):
    account = await get_account(account_id, db)
    if not account:
        raise Exception("Account not found")

    for field, value in field_params:
        setattr(account, field, value)

    await db.commit()
    await db.refresh(account)
    return account