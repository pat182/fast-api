
# from sqlalchemy.sql.annotation import Annotated

from app.db.models import Parlon, ParlonCategories
from app.core.base_repo import BaseRepo
from app.return_schemas import ParlonUpdateRequest,ParlonRequest

class ParlonRepository(BaseRepo):

    @property
    def model(self):
        return Parlon

    def apply_search(self, query, search: str | None):
        if search:
            return query.filter(self.model.business_name.ilike(f"%{search}%"))
        return query

    def create_parlon(self,request: ParlonRequest):

        parlon_data = request.model_dump(exclude={"category_ids"})
        new_parlon = self.model(**parlon_data)

        for cat_id in request.category_ids:
            new_parlon.parlon_categories.append(ParlonCategories(main_category_id=cat_id))

        self.db.add(new_parlon)

        return new_parlon
    #
    def get_by_business_name_country_id(self, business_name: str, country_id: int) -> Parlon | None :
        return self.db.query(Parlon).filter(
            Parlon.business_name == business_name,
            Parlon.country_id == country_id
        ).one_or_none()









