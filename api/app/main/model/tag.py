from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(45), nullable=True)
    type = Column(String(45), nullable=True)
