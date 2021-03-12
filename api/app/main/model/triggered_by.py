from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from . import Base


class TriggeredBy(Base):
    __tablename__ = 'triggered_by'
    display_rules_id = Column(Integer, ForeignKey('display_rules.id'))
    criterion_id = Column(Integer, ForeignKey('criterion.id'), primary_key=True)
    value_id = Column(Integer, ForeignKey('value.id'))
    path = Column(String)
