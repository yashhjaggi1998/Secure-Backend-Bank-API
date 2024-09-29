from fastapi import logger
from app.banking.constants import TRANSACTION_LIMIT
from app.banking.domain.response.ledger import *
from app.banking.repository import *
from app.banking.typings import TransactionType

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

class LedgerService:

    allTransactions = [
        {
            "account_id": "1",
            "transaction_id": "1",
            "transaction_type": "deposit",
            "amount": 2000
        },
        {
            "account_id": "1",
            "transaction_id": "2",
            "transaction_type": "withdrawal",
            "amount": 1000
        },
        {
            "account_id": "2",
            "transaction_id": "3",
            "transaction_type": "deposit",
            "amount": 1000
        },
        {
            "account_id": "2",
            "transaction_id": "4",
            "transaction_type": "withdrawal",
            "amount": 500
        }
    ]

    async def get_balance(self, account_id, db: AsyncSession):
        account = await get_account(account_id, db)
        if not account:
            raise Exception("Account not found")
        
        return account.balance

    async def add_transaction(self, transaction, db: AsyncSession):
        account_id, transaction_type, amount = transaction["account_id"], transaction["transaction_type"], transaction["amount"]
        if amount < 0:
            raise Exception("Amount cannot be negative")
        
        if transaction_type == TransactionType.DEPOSIT:
            if amount > TRANSACTION_LIMIT:
                raise Exception("Transaction limit exceeded")
        elif transaction_type == TransactionType.WITHDRAWAL:
            balance = await self.get_balance(account_id, db)
            if balance < amount:
                raise Exception("Insufficient balance")
            
        transaction = await create_transaction(account_id, transaction_type, amount, db)
        return transaction


    async def get_all_transactions(self, db: AsyncSession) -> List[Transaction]:
        all_transactions: List[Transaction] = await get_all_transactions(db)
        if len(all_transactions) == 0:
            raise Exception("No transactions found")
        
        return [Transaction.from_orm(transaction) for transaction in all_transactions]
    

    async def get_transactions_by_account_id(self, account_id: int, db: AsyncSession) -> List[Transaction]:
        all_transactions = await get_transactions_by_account_id(account_id, db)
        if len(all_transactions) == 0:
            raise Exception("No transactions found for the given account id")
        
        return [Transaction.from_orm(transaction) for transaction in all_transactions]
    

    async def get_transactions_by_type(self, transaction_type: str, db: AsyncSession) -> List[Transaction]:
        if transaction_type not in [TransactionType.DEPOSIT, TransactionType.WITHDRAWAL]:
            raise Exception("Invalid transaction type")
        
        all_transactions = await get_transactions_by_type(transaction_type, db)

        if len(all_transactions) == 0:
            raise Exception("No transactions found for the given transaction type")
        
        return [Transaction.from_orm(transaction) for transaction in all_transactions]


    async def reverse_transaction(self, transaction_id: int, db: AsyncSession) -> Transaction:
        transaction = await get_transaction_by_id(transaction_id, db)
        if not transaction:
            raise Exception("Transaction not found")
        
        if transaction.type == TransactionType.DEPOSIT:
            fields = [("type", TransactionType.WITHDRAWAL.value)]
        else:
            fields = [("type", TransactionType.DEPOSIT.value)]

        transaction = await update_transaction_fields(transaction_id, fields, db)
        
        return Transaction.from_orm(transaction)
    
    
    async def get_transaction_summary_by_account_id(self, account_id: int, db: AsyncSession) -> GetTransactionSummaryResponseBody:
        totalDeposits, totalWithdrawals, numberOfDeposits, numberOfWithdrawals = 0, 0, 0, 0

        all_transactions = await get_transactions_by_account_id(account_id, db)
        for transaction in all_transactions:
            if transaction.type == TransactionType.DEPOSIT:
                totalDeposits += transaction.amount
                numberOfDeposits += 1
            else:
                totalWithdrawals += transaction.amount
                numberOfWithdrawals += 1
        
        return GetTransactionSummaryResponseBody(
            total_deposits = totalDeposits,
            total_withdrawals = totalWithdrawals,
            number_of_deposits = numberOfDeposits,
            number_of_withdrawals = numberOfWithdrawals
        )
    
    
    async def validate_account_balance(self, account_id: int, db: AsyncSession) -> GetValidateAccountIdResponse:
        balance = await self.get_balance(account_id, db)

        accountTransactions = await get_transactions_by_account_id(account_id, db)
        balanceFromTransactions = 0
        for transaction in accountTransactions:
            if transaction.type == TransactionType.DEPOSIT:
                balanceFromTransactions += transaction.amount
            else:
                balanceFromTransactions -= transaction.amount

        return GetValidateAccountIdResponse(
            accountId = account_id,
            accountBalance = balance,
            balanceFromTransactions = balanceFromTransactions,
            isValid = balance == balanceFromTransactions
        )