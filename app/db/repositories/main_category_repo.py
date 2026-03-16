from sqlalchemy.orm import Session, Query

from app.core.base_repo import BaseRepo
from app.db.models import MainCategory

class MainCategoryRepository(BaseRepo):

    @property
    def model(self):
        return MainCategory

    def apply_search(self, query, search: str | None) -> Query:
        return query












