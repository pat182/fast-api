from sqlalchemy.orm import Session, Query
from app.db.models import Parlon

class ParlonRepository:

    def __init__(self, db: Session) :
        self.db = db

    def create_parlon(self, business_name: str, country_id: int) -> Parlon:
        new_parlon = Parlon(business_name=business_name, country_id=country_id)
        self.db.add(new_parlon)
        self.db.commit()
        self.db.refresh(new_parlon)
        return new_parlon

    def query(self) -> Query[type[Parlon]]:
        return self.db.query(Parlon)

    def get_by_business_name_country_id(self, business_name: str, country_id: int) -> Parlon | None :
        return self.db.query(Parlon).filter(
            Parlon.business_name == business_name,
            Parlon.country_id == country_id
        ).one_or_none()

    def filter_parlon(self,page: int, page_size: int, sort_by: str | None,sort_order: str | None,search: str | None
    ) -> tuple[list[type[Parlon]], int]:
        query = self.db.query(Parlon)

        if search:
            query = query.filter(Parlon.business_name.ilike(f"%{search}%"))

        if sort_by:
            sort_col = getattr(Parlon, sort_by, None)
            if sort_col is not None:
                if sort_order == "asc":
                    query = query.order_by(sort_col.asc())
                else:
                    query = query.order_by(sort_col.desc())

        total = query.count()
        data = query.offset((page - 1) * page_size).limit(page_size).all()

        return data, total

    def get_by_uuid(self,uuid:str) -> Parlon | None :
        return self.db.query(Parlon).filter(Parlon.id == uuid).one_or_none()






