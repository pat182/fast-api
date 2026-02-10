from typing import Annotated

from fastapi import APIRouter, Depends, Response,Request,Cookie
from sqlalchemy.orm import Session

from app.core.security import SecurityInstance
from app.schemas import LoginRequest, TokenResponse, UserResponse,Tokens,AppTokens
from app.db.database import get_db
from app.core.config import settings
from app.utils.helper import set_auth_cookies,clear_auth_cookies
from app.services.auth import AuthService

router = APIRouter(
    prefix=f"{settings.API_PREFIX}/v1/auth"
)

@router.post("/app/login",response_model=TokenResponse)
def app_login(request: LoginRequest, db: Annotated[Session, Depends(get_db)], response: Response):

    auth = AuthService(db, response,'app')
    token_data = auth.access_tokens(email=request.email, password=request.password, remember_me=request.remember_me)

    return TokenResponse(
        token=AppTokens(**token_data),
        csrf=None,
        user=token_data['user']
    )


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Annotated[Session, Depends(get_db)], response: Response):

    auth = AuthService(db,response)
    token_data = auth.access_tokens(email=request.email,password=request.password,remember_me=request.remember_me)
    # return token_data
    set_auth_cookies(
        response,
        access_token=token_data['access_token'],
        refresh_token=token_data['refresh_token'],
        csrf_token=token_data['csrf_token'],
        access_exp=token_data['expires_in'],
        refresh_exp=token_data['r_expires_in'],
    )

    return TokenResponse(
        token=Tokens(**token_data),
        csrf=token_data['csrf_token'],
        user=token_data['user']
    )
@router.post("/refresh",response_model=TokenResponse)
#
def refresh(
    response: Response,
    request : Request,
    db: Session = Depends(get_db),
    refresh_token: str = Cookie(None),
):

    auth = AuthService(db,response)
    payload = SecurityInstance.token_validation(request,'refresh')

    token_data = auth.refresh_tokens(
        refresh_token, payload
    )
    if payload.get('client_type') == 'browser':
        token_response = Tokens(**token_data)
        set_auth_cookies(
            response,
            access_token=token_data['access_token'],
            refresh_token=token_data['refresh_token'],
            csrf_token= token_data['csrf_token'] if token_data['csrf_token'] else request.headers.get("X-CSRF-Token"),
            access_exp=token_data['expires_in'],
            refresh_exp=token_data['r_expires_in']
        )
    else:
        token_response = AppTokens(**token_data)

    return TokenResponse(
        token=token_response,
        csrf=token_data['csrf_token'],
        user=UserResponse.model_validate(token_data['user'])
    )

@router.post("/logout")
def logout(response: Response):

    clear_auth_cookies(response)
    return {"detail": "Successfully logged out"}
