from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from .base_class import Base


class TriggeredBy(Base):
    __tablename__ = 'triggered_by'
    id = Column(Integer, primary_key=True, autoincrement=True)
    display_rules_id = Column(Integer, ForeignKey('display_rules.id'))
    criterion_id = Column(Integer, ForeignKey('criterion.id'))
    value_id = Column(Integer, ForeignKey('value.id'))
    path = Column(String, nullable=True)
    active = Column(Boolean, nullable=True)
