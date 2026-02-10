from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.role import RoleResponse
from app.schemas.parlon import ParlonResponse

class UserResponse(BaseModel):
    id: int
    email: str
    password: str
    verified: bool
    create_date: datetime
    update_date: datetime
    role : RoleResponse
    parlon : Optional[ParlonResponse] = None


    model_config = ConfigDict(from_attributes=True)