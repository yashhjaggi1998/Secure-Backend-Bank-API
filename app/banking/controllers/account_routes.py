from fastapi import APIRouter, Depends

from app.banking.service.account_service import AccountService

from app.banking.domain.request import *
from app.banking.domain.response.accounts import *

from app.auth.models import User
from app.auth.oauth2 import get_current_active_user

from app.db_connector import get_db
from sqlalchemy.ext.asyncio import AsyncSession

# Create a router instance for user routes
router = APIRouter()

account_service = AccountService()

@router.get("/{account_id}", response_model = AccountResponseBody )
async def get_account(account_id: int, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        account = await account_service.get_account(account_id, db)
        return account
    except Exception as e:
        return {"error": str(e)}


@router.post("/create", response_model = AccountResponseBody)
async def create_account(request: CreateAccountRequestBody, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        if not request.name or not request.balance:
            return {"error": "Invalid request body"}
    
        params = (request.name, request.balance)
        account = await account_service.create_account(params, db)
        return account
    except Exception as e:
        return {"error": str(e)}


@router.patch("/update", response_model = AccountResponseBody)
async def update_account(request: UpdateAccountRequestBody, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        if not request.account_id:
            return {"error": "Invalid request body"}
        
        field_params = []
        for key, value in request.model_dump().items():
            if key != "account_id":
                field_params.append((key, value))
        
        account = await account_service.update_account(request.account_id, field_params, db)

        if not account:
            return {"error": "Error updating account name"}
        
        return account
    except Exception as e:
        return {"error": str(e)}


@router.delete("/delete/{account_id}")
async def delete_account(account_id: int, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        if not account_id:
            return {"error": "Invalid request"}
        
        await account_service.delete_account(account_id, db)
        return {"message": "Account deleted successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.post("/deposit", response_model = AccountResponseBody)
async def deposit(request: BankingDepositWithdrawRequestBody, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        account_id, amount = request.account_id, request.amount
        account = await account_service.deposit(account_id, amount, db)

        if not account:
            return {"error": "Error depositing amount"}
    
        return account
    except Exception as e:
        return {"error": str(e)}
    
@router.post("/withdraw", response_model = AccountResponseBody)
async def withdraw(request: BankingDepositWithdrawRequestBody, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        account_id, amount = request.account_id, request.amount

        if amount < 0:
            return {"error": "Amount cannot be negative"}
        
        account = await account_service.withdraw(account_id, amount, db)
        return account
    except Exception as e:
        return {"error": str(e)}
    