from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship, backref

from . import Base


class CriterionHasValue(Base):
    __tablename__ = 'criterion_has_value'
    criterion_id = Column(Integer, ForeignKey('criterion.id'), primary_key=True)
    criterion = relationship("Criterion", backref=backref("values"))

    value_id = Column(Integer, ForeignKey('value.id'), primary_key=True)
    value = relationship("Value", backref=backref("criteria"))

    create_date = Column(DateTime, nullable=True)