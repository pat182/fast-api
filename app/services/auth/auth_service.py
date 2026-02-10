import secrets, uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from fastapi import Response

from app.core.security import SecurityInstance
from app.db.models import User
from app.utils import clear_auth_cookies
from app.exceptions import UnAuthorized

class AuthService:
    def __init__(self, db: Session,response : Response,client_type: str = 'browser'):
        self.db = db
        self.response = response
        self.client_type = client_type

    def access_tokens(self, email: str, password: str, remember_me: bool = False) -> dict:
        user = self.db.query(User).filter(User.email == email).first()
        csrf_token = secrets.token_urlsafe(32)
        if not user or not SecurityInstance.verify_password(password, user.password):
            raise UnAuthorized("Invalid credentials")

        # (short-lived)
        access_token_expires = timedelta(minutes=SecurityInstance.jwt_min)
        access_token = SecurityInstance.create_token(
            data={
                "sub": str(user.id),
                "role_id": user.role_id,
                "client_type": self.client_type,
                "type": "access"
            },
            expires_delta=access_token_expires
        )
        # breakpoint()
        expires_at = datetime.now(timezone.utc) + access_token_expires

        # (long-lived)
        refresh_token_expires = timedelta(days=SecurityInstance.jwt_refresh_days)
        refresh_token = SecurityInstance.create_token(
            data={
                "sub": str(user.id),
                "remember_me": remember_me,
                "type": "refresh",
                "client_type": self.client_type,
                "jti": str(uuid.uuid4()),  # <-- added unique ID
                "iat": datetime.now(timezone.utc).timestamp()  # <-- added issued-at
            },
            expires_delta=refresh_token_expires
        )
        r_expires_at = datetime.now(timezone.utc) + refresh_token_expires


        return {
            "access_token": access_token,
            "expires_in": int(access_token_expires.total_seconds()),
            "expires_at": f"{expires_at} UTC",
            "refresh_token": refresh_token,
            "r_expires_in": int(refresh_token_expires.total_seconds()),
            "r_expires_at": f"{r_expires_at} UTC",
            "csrf_token": csrf_token,
            "user": user
        }

    def refresh_tokens(self, refresh_token: str,payload : dict) -> dict:
        if not refresh_token:
            raise UnAuthorized("Missing refresh token")

        payload = payload

        if payload.get("type") != "refresh":
            clear_auth_cookies(self.response)
            raise UnAuthorized("Invalid token type")


        user = self.db.query(User).filter(User.id == int(payload.get("sub"))).first()
        if not user:
            clear_auth_cookies(self.response)
            raise UnAuthorized(status_code=404, msg="User not found")

        csrf_token = None
        remember_me = payload.get("remember_me", False)

        access_token_expires = timedelta(minutes=SecurityInstance.jwt_min)
        access_token = SecurityInstance.create_token(
            data={
                "sub": str(user.id),
                "role_id": user.role_id,
                "client_type": payload.get("client_type"),
                "type": "access"
            },
            expires_delta=access_token_expires
        )
        expires_at = datetime.now(timezone.utc) + access_token_expires

        if remember_me:
            refresh_token_expires = timedelta(days=SecurityInstance.jwt_refresh_days)
            new_refresh_token = SecurityInstance.create_token(
                data={
                    "sub": str(user.id),
                    "remember_me": True,
                    "type": "refresh",
                    "client_type": payload.get("client_type"),
                    "jti": str(uuid.uuid4()),
                    "iat": datetime.now(timezone.utc).timestamp()
                },
                expires_delta=refresh_token_expires
            )
            csrf_token = secrets.token_urlsafe(32)
            refresh_expires_at = datetime.now(timezone.utc) + refresh_token_expires
        else:
            new_refresh_token = refresh_token
            refresh_expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

        return {
            "csrf_token": csrf_token,
            'access_token' : access_token,
            "expires_in": int(access_token_expires.total_seconds()),
            "expires_at": f"{expires_at} UTC",
            'refresh_token': new_refresh_token,
            "r_expires_in": int((refresh_expires_at - datetime.now(timezone.utc)).total_seconds()),
            "r_expires_at": f"{refresh_expires_at} UTC",
            "user": user
        }