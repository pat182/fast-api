import uuid

from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Parlon(Base):
    __tablename__ = "parlons"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_name = Column(String(255), nullable=False, index=True)
    country_id = Column(ForeignKey("countries.id"), nullable=False)
    logo = Column(String(255), nullable=True)
    create_date = Column(DateTime, server_default=func.now(), nullable=False)
    update_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    users = relationship("User", back_populates="parlon")
    country = relationship("Country", back_populates="parlons")
