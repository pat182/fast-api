from typing import Annotated,Optional,List
from pydantic import BaseModel, constr



class ParlonRequest(BaseModel):
    business_name: Annotated[str,constr(min_length=1, max_length=100)]
    visibility: bool = False
    country_id: int
    category_ids: List[int]

class ParlonUpdateRequest(BaseModel):
    business_name: Optional[constr(min_length=1, max_length=100)] = None
    country_id: Optional[int] = None
    visibility: bool = False
    category_ids: List[int] = None





