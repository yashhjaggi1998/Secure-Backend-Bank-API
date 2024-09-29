from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.auth.models import User
from app.auth.oauth2 import get_current_active_user
from app.banking.service.ledger_service import LedgerService

from app.banking.domain.request import *
from app.banking.domain.response.ledger import *
from app.banking.domain.response.error_response import ErrorResponse

from app.db_connector import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Union

# Create a router instance for user routes
router = APIRouter()

ledgerService = LedgerService()

@router.get("/", response_model = Union[List[Transaction], ErrorResponse])
async def get_all_transaction(current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        all_transactions = await ledgerService.get_all_transactions(db)
        return all_transactions
    except Exception as e:
        error_response = ErrorResponse(
            error_code = 404, 
            message = str(e)
        )
        return JSONResponse(status_code = error_response.error_code, content = error_response.dict())
    

@router.get("/{account_id}", response_model = Union[List[Transaction], ErrorResponse])
async def get_transactions_by_account_id(account_id: int, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        all_transactions = await ledgerService.get_transactions_by_account_id(account_id, db)
        return all_transactions
    except Exception as e:
        error_response = ErrorResponse(
            error_code = 404, 
            message = str(e)
        )
        return JSONResponse(status_code = error_response.error_code, content = error_response.dict())
    

@router.get("/type/{transaction_type}", response_model = Union[List[Transaction], ErrorResponse])
async def get_transactions_by_type(transaction_type: str, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        all_transactions = await ledgerService.get_transactions_by_type(transaction_type, db)
        return all_transactions
    except Exception as e:
        error_response = ErrorResponse(
            error_code = 404,
            message = str(e)
        )
        return JSONResponse(status_code = error_response.error_code, content = error_response.dict())


@router.patch("/reverse", response_model = Union[Transaction, ErrorResponse])
async def reverse_transaction(request: ReverseTransactionRequestBody, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        transaction_id = request.transaction_id
        if transaction_id is None:
            raise Exception("Transaction id is required")
        
        transaction = await ledgerService.reverse_transaction(transaction_id, db)
        if transaction is None:
            raise Exception("Transaction not found")

        return transaction
    except Exception as e:
        error_response = ErrorResponse(
            error_code = 404,
            message = str(e)
        )
        return JSONResponse(status_code = error_response.error_code, content = error_response.dict())


@router.get("/summary/{account_id}", response_model = Union[GetTransactionSummaryResponseBody, ErrorResponse])
async def get_transaction_summary(account_id: int, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        if account_id is None:
            raise Exception("Account id is required")
        
        summary = await ledgerService.get_transaction_summary_by_account_id(account_id, db)
        if summary is None:
            raise Exception("No transactions found for the given account id")
        
        return summary
    except Exception as e:
        error_response = ErrorResponse(
            error_code = 404,
            message = str(e)
        )
        return JSONResponse(status_code = error_response.error_code, content = error_response.dict())
    

@router.get("/validate/{account_id}", response_model = Union[GetValidateAccountIdResponse, ErrorResponse])
async def validate_account(account_id: int, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    try:
        validAccountInfo = await ledgerService.validate_account_balance(account_id, db)
        return validAccountInfo
    except Exception as e:
        error_response = ErrorResponse(
            error_code = 404,
            message = str(e)
        )
        return JSONResponse(status_code = error_response.error_code, content = error_response.dict())
