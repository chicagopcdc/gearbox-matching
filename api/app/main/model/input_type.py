from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt

class InputType(Base):
    __tablename__ = 'input_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(45), nullable=True)
    name = Column(String(45), nullable=True)
