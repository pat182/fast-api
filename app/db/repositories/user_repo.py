from sqlalchemy.orm import Session
from app.core.base_repo import BaseRepo
from app.db.models.user import User

class UserRepo(BaseRepo):

    @property
    def model(self):
        return User
