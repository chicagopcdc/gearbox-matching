from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from gearbox.util.types import EligibilityCriteriaStatus 
from sqlalchemy.types import Enum as SQLEnum

from .base_class import Base


class EligibilityCriteria(Base):
    __tablename__ = 'eligibility_criteria'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    create_date = mapped_column(DateTime, nullable=True)
    status : Mapped[EligibilityCriteriaStatus] = mapped_column(SQLEnum(EligibilityCriteriaStatus), unique=False, nullable=False)

    notes = relationship("EligibilityCriteriaHasNote", back_populates="eligibility_criteria")
    el_criteria_has_criterions = relationship("ElCriteriaHasCriterion", back_populates="eligibility_criteria")
    study_version = relationship("StudyVersion", back_populates="eligibility_criteria")
    raw_criteria = relationship("RawCriteria", back_populates="eligibility_criteria")
