from fastapi import APIRouter, Depends

from app.auth.models import User
from app.auth.oauth2 import get_current_active_user
from app.banking.service.ledger_service import LedgerService

from app.banking.domain.request import *
from app.banking.domain.response.ledger import *


# Create a router instance for user routes
router = APIRouter()

ledgerService = LedgerService()

@router.get("/", response_model = GetAllTransactionsResponseBody)
def get_all_transaction(current_user: User = Depends(get_current_active_user)):
    try:
        allTransactions = ledgerService.get_all_transactions()

        if len(allTransactions) == 0:
            return {"error": "No transactions found"}
        
        return GetAllTransactionsResponseBody(transactions = allTransactions)
    except KeyError:
        return {"error": "Error occurred while fetching transactions"}
    
@router.get("/{account_id}", response_model = GetAllTransactionsResponseBody)
def get_transactions_by_account_id(account_id: str, current_user: User = Depends(get_current_active_user)):
    try:
        transactions = ledgerService.get_transactions_by_account_id(account_id)

        if len(transactions) == 0:
            return {"error": "No transactions found for the given account id"}
        
        return GetAllTransactionsResponseBody(transactions = transactions)
    except:
        return {"error": "Error occurred while fetching transactions by account id"}
    

@router.get("/type/{transaction_type}", response_model = GetAllTransactionsResponseBody)
def get_transactions_by_type(transaction_type: str, current_user: User = Depends(get_current_active_user)):
    try:
        if transaction_type not in ["deposit", "withdrawal"]:
            return {"error": "Invalid transaction type"}

        transactions = ledgerService.get_transactions_by_type(transaction_type)

        if len(transactions) == 0:
            return {"error": "No transactions found for the given transaction type"}
        
        return GetAllTransactionsResponseBody(transactions = transactions)
    except:
        return {"error": "Error occurred while fetching transactions by type"}
    

@router.patch("/reverse", response_model = Transaction)
def reverse_transaction(request: ReverseTransactionRequestBody, current_user: User = Depends(get_current_active_user)):
    try:
        transaction_id = request.transaction_id

        if transaction_id is None:
            return {"error": "Transaction id is required"}
        
        transaction = ledgerService.reverse_transaction(transaction_id)

        if transaction is None:
            return {"error": "Transaction not found"}

        return transaction
    except:
        return {"error": "Error occurred while reversing transaction"}
    
@router.get("/summary/{account_id}", response_model = GetTransactionSummaryResponseBody)
def get_transaction_summary(account_id: str, current_user: User = Depends(get_current_active_user)):
    try:
        if account_id is None:
            return {"error": "Account id is required"}
        
        summary = ledgerService.get_transaction_summary_by_account_id(account_id)

        if summary is None:
            return {"error": "No transactions found for the given account id"}
        
        return GetTransactionSummaryResponseBody(**summary)
    except:
        return {"error": "Error occurred while fetching transaction summary"}
    
@router.get("/validate/{account_id}", response_model = GetValidateAccountIdResponse)
def validate_account_id(account_id: str, current_user: User = Depends(get_current_active_user)):
    try:
        if account_id is None:
            return {"error": "Account id is required"}
        
        if not any(transaction["account_id"] == account_id for transaction in ledgerService.get_all_transactions()):
            return {"error": "Account id not found"}

        return ledgerService.validate_account_balance(account_id)
    except KeyError:
        return {"error": "Error occurred while validating account id"}
