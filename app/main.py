from datetime import timedelta
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.oauth2 import authenticate_user, create_access_token, get_current_active_user
from app.auth.oauth2 import ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme
from app.auth.models import Token, User
from app.auth.oauth2 import fake_users_db

from app.banking.controllers import account_router, ledger_router


app = FastAPI()


# Include the router instance in the app
app.include_router(account_router, prefix = "/banking/accounts", tags = ["Accounts"])
app.include_router(ledger_router, prefix = "/banking/ledger", tags = ["Ledger"])

# for security
@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/")
def read_root(token: Annotated[str, Depends(oauth2_scheme)]):
    return {
        "message": "Welcome to the Banking API",
        "oauth_token": token
    }

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
