from sqlalchemy import ForeignKey, Integer, DateTime, String
from sqlalchemy.orm import relationship, mapped_column
from gearbox.util.types import StudyVersionStatus
from sqlalchemy.dialects.postgresql import ENUM

from .base_class import Base


class StudyVersion(Base):
    __tablename__ = "study_version"

    id = mapped_column(Integer, primary_key=True)
    study_id = mapped_column(Integer, ForeignKey('study.id'))
    study_version_num = mapped_column(Integer, nullable=False)
    create_date = mapped_column(DateTime, nullable=True)
    status = mapped_column(ENUM(StudyVersionStatus), unique=False, nullable=False)
    eligibility_criteria_id = mapped_column(Integer, ForeignKey('eligibility_criteria.id', name='fk_eligibility_criteria_id'))
    study_algorithm_engine_id = mapped_column(Integer, ForeignKey('study_algorithm_engine.id', name='fk_study_algorithm_engine_id'), nullable=True)
    comments = mapped_column(String, nullable=True)

    eligibility_criteria = relationship("EligibilityCriteria", back_populates="study_version", lazy="joined")
    study_algorithm_engine = relationship("StudyAlgorithmEngine", back_populates="study_version", lazy="joined")
    study = relationship("Study", back_populates="study_versions", lazy="joined")
