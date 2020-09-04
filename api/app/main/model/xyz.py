from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt

class Xyz(Base):
    __tablename__ = 'xyz'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=True)
    code = Column(String(45), nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
