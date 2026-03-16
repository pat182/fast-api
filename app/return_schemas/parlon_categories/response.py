from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.return_schemas.main_categories import MainCategoriesResponse

class ParlonCategoriesResponse(BaseModel):
        main_category : MainCategoriesResponse
        create_date: datetime
        update_date: datetime

        model_config = ConfigDict(from_attributes=True)