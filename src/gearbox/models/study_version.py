from sqlalchemy import ForeignKey, Column, Integer, DateTime, String
from sqlalchemy.orm import relationship
from gearbox.util.types import StudyVersionStatus
from sqlalchemy.dialects.postgresql import ENUM

from .base_class import Base


class StudyVersion(Base):
    __tablename__ = "study_version"

    id = Column(Integer, primary_key=True)
    study_id = Column(Integer, ForeignKey('study.id'))
    study_version_num = Column(Integer, nullable=False)
    create_date = Column(DateTime, nullable=True)
    status = Column(ENUM(StudyVersionStatus), unique=False, nullable=True)
    eligibility_criteria_id = Column(Integer, ForeignKey('eligibility_criteria.id', name='fk_eligibility_criteria_id'))
    study_algorithm_engine_id = Column(Integer, ForeignKey('study_algorithm_engine.id', name='fk_study_algorithm_engine_id'), nullable=True)
    comments = Column(String, nullable=True)

    eligibility_criteria = relationship("EligibilityCriteria", back_populates="study_version", lazy="joined")
    study_algorithm_engine = relationship("StudyAlgorithmEngine", back_populates="study_version", lazy="joined")
    study = relationship("Study", back_populates="study_versions", lazy="joined")
