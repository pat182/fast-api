from datetime import datetime

from sqlalchemy import Column, String,Integer, DateTime, func
from app.db.database import Base
from sqlalchemy.orm import relationship

class MainCategory(Base):
    __tablename__ = "main_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    create_date = Column(DateTime, server_default=func.now(), nullable=False)
    update_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    parlon_categories = relationship("ParlonCategories", back_populates="main_category")




