from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base


class EligibilityCriteria(Base):
    __tablename__ = 'eligibility_criteria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
    study_version_id = Column(Integer, ForeignKey('study_version.id'))

    notes = relationship("EligibilityCriteriaHasNote", back_populates="eligibility_criteria")
    criterions = relationship("ElCriteriaHasCriterion", back_populates="eligibility_criteria")
    values = relationship("ElCriteriaHasCriterion", back_populates="eligibility_criteria")
