
from sqlalchemy.orm import Session, Query
from app.db.models import Country
from app.core.base_repo import BaseRepo
from sqlalchemy import exists

class CountryRepository(BaseRepo):

    @property
    def model(self):
        return Country








