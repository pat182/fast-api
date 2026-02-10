from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.core.config import settings

router = APIRouter(
    prefix=f"{settings.API_PREFIX}/v1/user"
)

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).limit(5).all()

