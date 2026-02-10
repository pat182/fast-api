from typing import Literal, Optional

from fastapi import APIRouter, Depends, Query,UploadFile
from sqlalchemy.orm import Session,joinedload

from app.core.config import settings
from app.dependencies import check_roles
from app.db.database import get_db

from app.exceptions import DataDoesNotExist
from app.services.parlon import ParlonService
from app.db.repositories import ParlonRepository
from app.schemas import ParlonResponse,PaginatedResponse,ParlonRequest,ParlonUpdateRequest

router = APIRouter(
    prefix=f"{settings.API_PREFIX}/v1",
    dependencies=[Depends( check_roles([1]) )]
)

PaginatedParlonResponse = PaginatedResponse[ParlonResponse]
@router.get("/parlons", response_model=PaginatedParlonResponse)
def index(
        page:int=Query(1,ge=1),
        page_size:int=Query(25,ge=1),
        db : Session = Depends(get_db),
        sort_by: Optional[Literal["business_name", "create_date", "update_date"]] = Query(None),
        sort_order: Optional[Literal["asc", "desc"]] = Query(None),
        search: Optional[str] = Query(None)
    ):

    repo = ParlonRepository(db)
    parlons, total = repo.filter_parlon(page, page_size, sort_by, sort_order, search)

    return PaginatedResponse(page=page, page_size=page_size, total_items=total, data=parlons)


@router.get("/parlons/{uuid}",response_model = ParlonResponse)
#
def show(uuid: str, db: Session = Depends(get_db)):

    parlon = ParlonRepository(db).get_by_uuid(uuid)
    if parlon is None:
        raise DataDoesNotExist(uuid)
    return parlon

@router.post("/parlons", response_model=ParlonResponse)
def create_parlon(
        request: ParlonRequest,
        db: Session = Depends(get_db)
):
        service = ParlonService(db)
        new_parlon = service.create_unique_parlon(request.business_name, request.country_id)
        return new_parlon

@router.put("/parlons/{uuid}", response_model=ParlonResponse)
def update_parlon(
    uuid: str,
    request: ParlonUpdateRequest,
    db: Session = Depends(get_db)
):
    service = ParlonService(db)
    updated_parlon = service.update_parlon(uuid, request)
    return updated_parlon

