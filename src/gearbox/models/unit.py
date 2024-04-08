from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from .base_class import Base


class Unit(Base):
    __tablename__ = 'unit'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)

    UniqueConstraint(name, name='unit_name_uix')
    values= relationship("Value", back_populates="unit")