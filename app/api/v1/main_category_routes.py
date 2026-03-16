from typing import Optional,Literal,List

from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,Query

from app import db
from app.core.config import settings
from app.dependencies import check_roles
from app.db.database import get_db
from app.db.repositories import MainCategoryRepository
from app.return_schemas import MainCategoriesResponse,PaginatedResponse
router = APIRouter(
    prefix=f"{settings.API_PREFIX}/v1",
    dependencies=[Depends( check_roles([1]) )]
)
@router.get("/categories/all",response_model=List[MainCategoriesResponse])
# response_model=MainCategoriesResponse
def all_categories(db : Session = Depends(get_db)):
    repo = MainCategoryRepository(db)
    return repo.get_all()

@router.get( "/categories",response_model=PaginatedResponse[MainCategoriesResponse])
#response_model=PaginatedResponse[MainCategoriesResponse]
def index(
        page:int=Query(1,ge=1),
        page_size:int=Query(25,ge=1),
        db : Session = Depends(get_db),
        sort_by: Optional[Literal["business_name", "create_date", "update_date"]] = Query(None),
        sort_order: Optional[Literal["asc", "desc"]] = Query(None),
        search: Optional[str] = Query(None)
):
    repo = MainCategoryRepository(db)
    categories, total = repo.filter(page, page_size, sort_by, sort_order, search)
    # return categories, total
    return PaginatedResponse(
        page=page,
        page_size=page_size,
        total_items=total,
        data=categories,
    )
