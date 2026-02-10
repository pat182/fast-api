from uuid import UUID
from datetime import datetime

from pydantic import BaseModel,ConfigDict

class ParlonResponse(BaseModel):
    id: UUID
    business_name: str
    create_date: datetime
    update_date: datetime

    model_config = ConfigDict(from_attributes=True)