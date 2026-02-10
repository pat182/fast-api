from fastapi import APIRouter, Depends

from app.core.config import settings
from app.db.models import User
from app.dependencies import check_roles
from app.schemas import UserResponse

router = APIRouter(
    prefix=f"{settings.API_PREFIX}/v1/me",
)

@router.get("/",response_model=UserResponse)
def auth_test(current_user: User = Depends(check_roles([1]))):
    return current_user
