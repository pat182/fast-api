from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.db.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    create_date = Column(DateTime, server_default=func.now(), nullable=False)
    update_date = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    users = relationship("User", back_populates="role")
