from sqlalchemy import Integer, String, DateTime, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class Unit(Base):
    __tablename__ = 'unit'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=True)

    UniqueConstraint(name, name='unit_name_uix')
    values= relationship("Value", back_populates="unit")
