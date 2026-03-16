from datetime import datetime

from pydantic import BaseModel

class CountryResponse(BaseModel):
    id : int
    country_name : str
    code : str
    create_date : datetime
    update_date : datetime