from typing import Union
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.banking.domain.response.error_response import ErrorResponse
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

@router.get("/{account_id}", response_model = Union[AccountResponseBody, ErrorResponse])
async def get_account(account_id: int, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        account = await account_service.get_account(account_id, db)
        return account
    except Exception as e:
        error_response = ErrorResponse(
            error_code = 404, 
            message = str(e)
        )
        return JSONResponse(status_code = error_response.error_code, content = error_response.dict())


@router.post("/create", response_model = Union[AccountResponseBody, ErrorResponse])
async def create_account(request: CreateAccountRequestBody, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        params = (request.name, request.balance)
        print(f"Creating account with name: {request.name}")
        account = await account_service.create_account(params, db)
        return account
    except Exception as e:
        error_response = ErrorResponse(
            error_code = 404, 
            message = str(e)
        )
        return JSONResponse(status_code = error_response.error_code, content = error_response.dict())


@router.patch("/update", response_model = Union[AccountResponseBody, ErrorResponse])
async def update_account(request: UpdateAccountRequestBody, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        if not request.account_id:
            return {"error": "Invalid request body"}
        
        field_params = []
        for key, value in request.model_dump().items():
            if key != "account_id" and value is not None:
                field_params.append((key, value))
        
        account = await account_service.update_account(request.account_id, field_params, db)

        if not account:
            return {"error": "Error updating account name"}
        
        return account
    except Exception as e:
        error_response = ErrorResponse(
            error_code = 404, 
            message = str(e)
        )
        return JSONResponse(status_code = error_response.error_code, content = error_response.dict())


@router.delete("/delete/{account_id}")
async def delete_account(account_id: int, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        if not account_id:
            return {"error": "Invalid request"}
        
        await account_service.delete_account(account_id, db)
        return {"message": "Account deleted successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.post("/deposit", response_model = Union[AccountResponseBody, ErrorResponse])
async def deposit(request: BankingDepositWithdrawRequestBody, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        account_id, amount = request.account_id, request.amount
        account = await account_service.deposit(account_id, amount, db)

        if not account:
            return {"error": "Error depositing amount"}
    
        return account
    except Exception as e:
        error_response = ErrorResponse(
            error_code = 404, 
            message = str(e)
        )
        return JSONResponse(status_code = error_response.error_code, content = error_response.dict())
    
    
@router.post("/withdraw", response_model = Union[AccountResponseBody, ErrorResponse])
async def withdraw(request: BankingDepositWithdrawRequestBody, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        account_id, amount = request.account_id, request.amount

        if amount < 0:
            return {"error": "Amount cannot be negative"}
        
        account = await account_service.withdraw(account_id, amount, db)
        return account
    except Exception as e:
        error_response = ErrorResponse(
            error_code = 404, 
            message = str(e)
        )
        return JSONResponse(status_code = error_response.error_code, content = error_response.dict())
    