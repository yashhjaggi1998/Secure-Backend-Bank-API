from fastapi import APIRouter, Depends

from app.banking.service.account_service import AccountService

from app.auth.models import User
from app.auth.oauth2 import get_current_active_user

from app.banking.domain.request.BankingDepositRequestBody import BankingDepositRequestBody
from app.banking.domain.response.accounts import *

# Create a router instance for user routes
router = APIRouter()

account_service = AccountService()

@router.get("/balance/{account_id}", response_model = GetAccountBalanceResponseBody)
def get_balance(account_id: str, current_user: User = Depends(get_current_active_user)):
    try:
        balance = account_service.get_balance(account_id)
        return {"balance": balance}
    except KeyError:
        return {"error": "Account not found"}

@router.get("/{account_id}", response_model = AccountResponseBody )
def get_account(account_id: str, current_user: User = Depends(get_current_active_user)):
    try:
        account = account_service.get_account(account_id)
        return account
    except KeyError:
        return {"error": "Account not found"}
    
@router.post("/deposit", response_model = AccountResponseBody)
def deposit(request: BankingDepositRequestBody, current_user: User = Depends(get_current_active_user)):
    try:
        account = account_service.deposit(request.account_id, request.amount)
        return account
    except:
        return {"error": "Error depositing amount"}
    
@router.post("/withdraw", response_model = AccountResponseBody)
def withdraw(request: BankingDepositRequestBody, current_user: User = Depends(get_current_active_user)):
    try:
        account_id, amount = request.account_id, request.amount

        if not account_id or not amount:
            return {"error": "Invalid request body"}
        
        account = account_service.withdraw(request.account_id, request.amount)
        return account
    except Exception as e:
        print(e)
        # return error message from variable e
        return {"error": str(e)}
    