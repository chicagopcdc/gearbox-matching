from sqlalchemy import ForeignKey, Column, Integer, Boolean, String
from sqlalchemy.orm import relationship

from .base_class import Base


class DisplayRules(Base):
    __tablename__ = 'display_rules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    criterion_id = Column(Integer, ForeignKey('criterion.id'))
    priority = Column(Integer)
    active = Column(Boolean, nullable=True)
    version = Column(Integer, nullable=True)

    triggered_bys = relationship("TriggeredBy", back_populates="display_rules", lazy="joined", order_by="TriggeredBy.id")
    criterion = relationship("Criterion", back_populates="display_rules", lazy="joined")