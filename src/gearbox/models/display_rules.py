from sqlalchemy import ForeignKey, Integer, Boolean, String
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class DisplayRules(Base):
    __tablename__ = 'display_rules'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    criterion_id = mapped_column(Integer, ForeignKey('criterion.id'))
    priority = mapped_column(Integer)
    active = mapped_column(Boolean, nullable=True)
    version = mapped_column(Integer, nullable=True)

    triggered_bys = relationship("TriggeredBy", back_populates="display_rules", lazy="joined", order_by="TriggeredBy.id")
    criterion = relationship("Criterion", back_populates="display_rules", lazy="joined")
