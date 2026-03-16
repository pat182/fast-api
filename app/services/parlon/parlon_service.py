from sqlalchemy.orm import Session

from app.db.models import Parlon,ParlonCategories
from app.db.repositories import ParlonRepository,CountryRepository,MainCategoryRepository
from app.exceptions import BusinessNameAlreadyExists,DataDoesNotExist
from app.return_schemas import ParlonUpdateRequest,ParlonRequest

class ParlonService:
    def __init__(self, db: Session):
        self.repo = ParlonRepository(db)
        self.country_repo = CountryRepository(db)
        self.main_category_repo = MainCategoryRepository(db)

    def create_unique_parlon(self,request: ParlonRequest) -> Parlon:

        if not self.country_repo.get_by_id(request.country_id):
            raise DataDoesNotExist(f"Country {request.country_id}")

        for cat_id in request.category_ids:
            if not self.main_category_repo.get_by_id(cat_id):
                raise DataDoesNotExist(f"Category {cat_id}")

        if self.repo.get_by_business_name_country_id(request.business_name,request.country_id):
            raise BusinessNameAlreadyExists(request.business_name)

        return self.repo.create_parlon(request)

    def update_parlon(self, uuid: str, request: ParlonUpdateRequest) -> Parlon:

        parlon = self.repo.get_by_id(uuid)
        if parlon is None:
            raise DataDoesNotExist(uuid)

        if request.country_id is not None and request.country_id != parlon.country_id:
            if not self.country_repo.get_by_id(request.country_id):
                raise DataDoesNotExist(request.country_id)
            parlon.country_id = request.country_id

        if request.business_name is not None and request.business_name != parlon.business_name:
            existing = self.repo.get_by_business_name_country_id(request.business_name,parlon.country_id)
            if existing and existing.id != parlon.id:
                raise BusinessNameAlreadyExists(request.business_name)
            parlon.business_name = request.business_name

        if request.visibility is not None:
            parlon.visibility = request.visibility

        if request.category_ids is not None:
            for cat_id in request.category_ids:
                if not self.main_category_repo.get_by_id(cat_id):
                    raise DataDoesNotExist(f"Category {cat_id}")

            parlon.parlon_categories.clear()

            for cat_id in request.category_ids:
                parlon.parlon_categories.append(ParlonCategories(parlon_id=parlon.id, main_category_id=cat_id))

        return parlon



