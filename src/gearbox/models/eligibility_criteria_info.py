from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship

from .base_class import Base


class EligibilityCriteriaInfo(Base):
    __tablename__ = 'eligibility_criteria_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
    study_version_id = Column(Integer, ForeignKey('study_version.id'))
    study_algorithm_engine_id = Column(Integer, ForeignKey('study_algorithm_engine.id'))
    eligibility_criteria_id = Column(Integer, ForeignKey('eligibility_criteria.id'))

    study_algorithm_engine = relationship("StudyAlgorithmEngine", back_populates="eligibility_criteria_info", lazy="joined")
    eligibility_criteria_id = relationship("EligibilityCriteria", back_populates="eligibility_criteria_info", lazy="joined")
    #notes = relationship("EligibilityCriteriaHasNote", back_populates="eligibility_criteria")
    #el_criteria_has_criterions = relationship("ElCriteriaHasCriterion", back_populates="eligibility_criteria")
    #infos = relationship("EligibilityCriteriaInfo", back_populates="eligibility_criteria")