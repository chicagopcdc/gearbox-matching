from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from . import Base


class DisplayRules(Base):
    __tablename__ = 'display_rules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    criterion_id = Column(Integer, ForeignKey('criterion.id'))
    priority = Column(Integer)
