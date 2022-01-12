from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from .base_class import Base

class Note(Base):
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String, nullable=True)
