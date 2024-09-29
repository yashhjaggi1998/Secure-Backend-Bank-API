from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.banking.typings import TransactionType
from ..domain.models.transaction_model import Transaction
from typing import List

async def get_all_transactions(db: AsyncSession):
    result = await db.execute(select(Transaction))
    transactions = result.scalars().all()
    return transactions

async def get_transaction_by_id(transaction_id: int, db: AsyncSession):
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
    transaction = result.scalars().first()
    return transaction

async def get_transactions_by_account_id(account_id: int, db: AsyncSession) -> List[Transaction]:
    result = await db.execute(select(Transaction).where(Transaction.account_id == account_id))
    transactions = result.scalars().all()
    return transactions

async def get_transactions_by_type(transaction_type: str, db: AsyncSession):
    transaction_type = transaction_type.upper()
    result = await db.execute(select(Transaction).where(Transaction.type == transaction_type))
    transactions = result.scalars().all()
    return transactions