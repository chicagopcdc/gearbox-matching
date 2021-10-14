from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base


class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    code = Column(String, nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)


