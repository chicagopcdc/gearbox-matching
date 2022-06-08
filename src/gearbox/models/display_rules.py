from sqlalchemy import ForeignKey, Column, Integer, Boolean, String
from sqlalchemy.orm import relationship

from .base_class import Base


class DisplayRules(Base):
    __tablename__ = 'display_rules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    criterion_id = Column(Integer, ForeignKey('criterion.id'))
    priority = Column(String, nullable=True)
    active = Column(Boolean, nullable=True)
    version = Column(Integer, nullable=True)

    # change table name from display_rules to display_rule?
    triggered_bys = relationship("TriggeredBy", back_populates="display_rules")
    criterion = relationship("Criterion", back_populates="display_rules")