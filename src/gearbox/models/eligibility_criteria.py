from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship
from gearbox.util.types import EligibilityCriteriaStatus 
from sqlalchemy.dialects.postgresql import ENUM

from .base_class import Base


class EligibilityCriteria(Base):
    __tablename__ = 'eligibility_criteria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_date = Column(DateTime, nullable=True)
    status = Column(ENUM(EligibilityCriteriaStatus), unique=False, nullable=False)

    notes = relationship("EligibilityCriteriaHasNote", back_populates="eligibility_criteria")
    el_criteria_has_criterions = relationship("ElCriteriaHasCriterion", back_populates="eligibility_criteria")
    study_version = relationship("StudyVersion", back_populates="eligibility_criteria")
    raw_criteria = relationship("RawCriteria", back_populates="eligibility_criteria")