from typing import Annotated,Optional
from pydantic import BaseModel, constr



class ParlonRequest(BaseModel):
    business_name: Annotated[str,constr(min_length=1, max_length=100)]
    country_id: int

class ParlonUpdateRequest(BaseModel):
    business_name: Optional[constr(min_length=1, max_length=100)] = None
    country_id: Optional[int] = None





