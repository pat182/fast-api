from sqlalchemy import Column, String,ForeignKey, DateTime, func,Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class ParlonCategories(Base):
    __tablename__ = "parlon_categories"

    parlon_id = Column(String(36), ForeignKey("parlons.id"), primary_key=True)
    main_category_id = Column(Integer, ForeignKey("main_categories.id"), primary_key=True)
    create_date = Column(DateTime, server_default=func.now(), nullable=False)
    update_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    parlon = relationship("Parlon", back_populates="parlon_categories")
    main_category = relationship("MainCategory", back_populates="parlon_categories")

