from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base

from app.main.model.criterion_has_tag import CriterionHasTag


class Criterion(Base):
    __tablename__ = 'criterion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(45), nullable=True)
    display_name = Column(String(45), nullable=True)
    description = Column(String(45), nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

    tags = relationship("CriterionHasTag", back_populates="criterion")
    eligibility_criterias = relationship("ElCriteriaHasCriterion", back_populates="criterion")
