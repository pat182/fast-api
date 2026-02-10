from sqlalchemy.orm import Session

from app.db.models import Parlon
from app.db.repositories import ParlonRepository,CountryRepository
from app.exceptions import BusinessNameAlreadyExists,DataDoesNotExist
from app.exceptions import DataDoesNotExist
from app.schemas import ParlonUpdateRequest
from app.utils import dd

class ParlonService:
    def __init__(self, db: Session):
        self.repo = ParlonRepository(db)
        self.country_repo = CountryRepository(db)
        self.db = db

    def create_unique_parlon(self, business_name: str, country_id: int) -> Parlon:

        if not self.country_repo.get_by_id(country_id):
            raise DataDoesNotExist(country_id)

        if self.repo.get_by_business_name_country_id(business_name,country_id):
            raise BusinessNameAlreadyExists(business_name)

        return self.repo.create_parlon(business_name, country_id)

    def update_parlon(self, uuid: str, request: ParlonUpdateRequest) -> Parlon:

        parlon = self.repo.get_by_uuid(uuid)
        if parlon is None:
            raise DataDoesNotExist(uuid)

        if request.country_id is not None:
            if not self.country_repo.get_by_id(request.country_id):
                raise DataDoesNotExist(request.country_id)
            parlon.country_id = request.country_id

        if request.business_name is not None:
            existing = self.repo.get_by_business_name_country_id(request.business_name,parlon.country_id)
            if existing and existing.id != parlon.id:
                raise BusinessNameAlreadyExists(request.business_name)
            parlon.business_name = request.business_name

        self.db.commit()
        self.db.refresh(parlon)

        return parlon



