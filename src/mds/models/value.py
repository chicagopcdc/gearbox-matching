from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from . import Base


class Value(Base):
    __tablename__ = 'value'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, nullable=True)
    description = Column(String, nullable=True)
    type = Column(String, nullable=True)
    value_string = Column(String, nullable=True)
    unit = Column(String, nullable=True)
    operator = Column(String, nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

