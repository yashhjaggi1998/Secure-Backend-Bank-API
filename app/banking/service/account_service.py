from app.banking.domain.models.account_model import Account
from app.banking.domain.response.accounts import AccountResponseBody

from app.banking.repository.get_account import get_account
from app.banking.repository.create_account import create_account
from app.banking.repository.update_account import update_account_fields
from app.banking.repository.delete_account import soft_delete_account

from sqlalchemy.ext.asyncio import AsyncSession

from app.banking.typings import *
from app.banking.constants import TRANSACTION_LIMIT


class AccountService:

    async def get_account(self, account_id: int, db: AsyncSession) -> AccountResponseBody:
        account = await get_account(account_id, db) 
        if not account:
            raise Exception("Account not found")
        
        return AccountResponseBody(
            account_id = account.id,
            account_name = account.name,
            balance = account.balance
        )
    

    async def create_account(self, account_params: CreateAccountParams, db: AsyncSession) -> AccountResponseBody:
        account_name, balance = account_params
        if balance < 0:
            raise Exception("Balance cannot be negative")
        
        account = await create_account(account_name, balance, db)

        if not account:
            raise Exception("Error creating account")
        
        return AccountResponseBody(
            account_id = account.id,
            account_name = account.name,
            balance = account.balance
        )
    

    async def update_account(self, account_id: int, fields: UpdateAccountFieldParams, db: AsyncSession) -> AccountResponseBody:
        for field, value in fields:
            if field == "balance":
                if value < 0:
                    raise Exception("Balance cannot be negative")
                if value > TRANSACTION_LIMIT:
                    raise Exception("Transaction limit exceeded")
            
        account = await update_account_fields(account_id, fields, db)
        if not account:
            raise Exception("Error updating account")
        
        return AccountResponseBody(
            account_id = account.id,
            account_name = account.name,
            balance = account.balance
        )
    

    async def delete_account(self, account_id: int, db: AsyncSession):
        deleted_account = await soft_delete_account(account_id, db) # hanldes the case where account_id is not found
       
        if not deleted_account or not deleted_account.deleted_at:
            raise Exception("Error deleting account")


    # I believe these must go in transactions service
    async def deposit(self, account_id: int, amount: float, db: AsyncSession) -> AccountResponseBody:
        if amount > TRANSACTION_LIMIT:
            raise Exception("Transaction limit exceeded")

        current_account: Account = await get_account(account_id, db)
        if not current_account:
            raise Exception("Account not found")
        
        current_balance: float = current_account.balance
        amount += current_balance
        field_params: UpdateAccountFieldParams = [("balance", amount)]
        account = await update_account_fields(account_id, field_params, db)

        if not account:
            raise Exception("Error depositing amount")
        
        return AccountResponseBody(
            account_id = account.id,
            account_name = account.name,
            balance = account.balance
        )
    
    # I believe these must go in transactions service
    async def withdraw(self, account_id, amount, db: AsyncSession):
        current_account: Account = await get_account(account_id, db)
        if not current_account:
            raise Exception("Account not found")
        
        current_balance: float = current_account.balance

        if amount > current_balance:
            raise Exception("Insufficient balance")
        
        amount = current_balance - amount
        field_params: UpdateAccountFieldParams = [("balance", amount)]
        account = await update_account_fields(account_id, field_params, db)

        if not account:
            raise Exception("Error withdrawing amount")
        
        return AccountResponseBody(
            account_id = account.id,
            account_name = account.name,
            balance = account.balance
        )