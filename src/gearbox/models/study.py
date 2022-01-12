from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from .base_class import Base

class Study(Base):
    __tablename__ = "study"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    code = Column(String, nullable=True)
    description = Column(String, nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

    sites = relationship("Site", secondary="site_has_study")
