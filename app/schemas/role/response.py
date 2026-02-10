from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RoleResponse(BaseModel):
    id: int
    name: str
    create_date: datetime
    update_date: datetime

    model_config = ConfigDict(from_attributes=True)