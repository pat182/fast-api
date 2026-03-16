
from app.core.base_repo import BaseRepo
from app.db.models import ParlonCategories

class ParlonCategoriesRepository(BaseRepo):
    @property
    def model(self):
        return ParlonCategories










