from sqlalchemy import ForeignKey, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class TriggeredBy(Base):
    __tablename__ = 'triggered_by'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    display_rules_id = mapped_column(Integer, ForeignKey('display_rules.id'))
    criterion_id = mapped_column(Integer, ForeignKey('criterion.id'))
    value_id = mapped_column(Integer, ForeignKey('value.id'))
    path = mapped_column(String, nullable=True)
    active = mapped_column(Boolean, nullable=True)

    display_rules = relationship("DisplayRules", back_populates="triggered_bys",lazy="joined")
    criterion = relationship("Criterion", back_populates="triggered_bys",lazy="joined")
    value = relationship("Value", back_populates="triggered_bys",lazy="joined")
