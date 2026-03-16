from typing import List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.return_schemas.parlon_categories import ParlonCategoriesResponse

class ParlonResponse(BaseModel):
    id: UUID
    business_name: str
    visibility : bool
    create_date: datetime
    update_date: datetime
    parlon_categories: List[ParlonCategoriesResponse]

    model_config = ConfigDict(from_attributes=True)
