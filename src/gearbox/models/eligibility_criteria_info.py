from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship

from .base_class import Base


class EligibilityCriteriaInfo(Base):
    __tablename__ = 'eligibility_criteria_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
    study_version_id = Column(Integer, ForeignKey('study_version.id', name='fk_study_version_id'))
    study_algorithm_engine_id = Column(Integer, ForeignKey('study_algorithm_engine.id', name='fk_study_algorithm_engine_id'))
    eligibility_criteria_id = Column(Integer, ForeignKey('eligibility_criteria.id', name='fk_eligibility_criteria_id'))

    study_algorithm_engine = relationship("StudyAlgorithmEngine", back_populates="eligibility_criteria_info", lazy="joined")
    eligibility_criteria = relationship("EligibilityCriteria", back_populates="eligibility_criteria_info", lazy="joined")
    study_version = relationship("StudyVersion", back_populates="eligibility_criteria_infos", lazy="joined")
