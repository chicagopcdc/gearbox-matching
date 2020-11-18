from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt

class Value(Base):
    __tablename__ = 'value'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(45), nullable=True)
    type = Column(String(45), nullable=True)
    display_value = Column(String(45), nullable=True)
    upper_threshold = Column(Float, nullable=True)
    lower_threshold = Column(Float, nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
