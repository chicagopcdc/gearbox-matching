from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from .base_class import Base


class StudyAlgorithmEngine(Base):
    __tablename__ = 'study_algorithm_engine'
    id = Column(Integer, primary_key=True, autoincrement=True)
    #study_version_id = Column(Integer, ForeignKey('study_version.id'))
    start_date = Column(DateTime, nullable=True)
    algorithm_logic = Column(JSON)
    algorithm_version = Column(Integer)
    # active = Column(Boolean, nullable=True)

    study_version = relationship("StudyVersion", back_populates="study_algorithm_engine")
    eligibility_criteria_infos = relationship("EligibilityCriteriaInfo", back_populates="study_algorithm_engine")