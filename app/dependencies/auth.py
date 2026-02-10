from typing import List, Annotated, Callable

from fastapi import Request, Depends
from sqlalchemy.orm import Session

from app.core.security import SecurityInstance
from app.db.database import get_db
from app.db.models import User
from app.exceptions import UnAuthorized

def auth_user(request: Request, db: Session = Depends(get_db)) -> type[User]:

    payload = SecurityInstance.token_validation(request)

    user_id = payload["sub"]
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise UnAuthorized("User not found",404)

    return user

def __verify_csrf(csrf_header: str, csrf_cookie: str):
    if not csrf_cookie or csrf_cookie != csrf_header:
        raise UnAuthorized("CSRF validation failed")

def check_roles(allowed_roles: List[int]) -> Callable[..., User]:
    def wrapper(user: User = Depends(auth_user)):
        if user.role_id not in allowed_roles:
            raise UnAuthorized(
                msg="You do not have the required permissions",
                status_code=403)
        return user
    return wrapper

