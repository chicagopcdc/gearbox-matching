from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship

from .base_class import Base


class StudyVersion(Base):
    __tablename__ = "study_version"

    id = Column(Integer, primary_key=True)
    study_id = Column(Integer, ForeignKey('study.id'))
    study_version = Column(Integer, nullable=False)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
  
    eligibility_criteria_infos = relationship("EligibilityCriteriaInfo", back_populates="study_version", lazy="joined")
    study = relationship("Study", back_populates="study_versions", lazy="joined")
