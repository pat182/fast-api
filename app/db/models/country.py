from datetime import datetime

from sqlalchemy import Column,String,DateTime,Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    country_name = Column(String(255), index=True)
    code = Column(String(5), unique=True)
    create_date = Column(DateTime, default=datetime.now)
    update_date = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    parlons = relationship("Parlon", back_populates="country")