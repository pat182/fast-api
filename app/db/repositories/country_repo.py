
from sqlalchemy.orm import Session, Query
from app.db.models import Country
from sqlalchemy import exists

class CountryRepository:

    def __init__(self, db: Session) :
        self.db = db

    def get_by_id(self, country_id: int) -> Country | None :
        return self.db.query(Country).filter(Country.id == country_id).one_or_none()







