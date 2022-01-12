from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship, backref

from .base_class import Base

class StudyVersion(Base):
    __tablename__ = "study_version"

    id = Column(Integer, primary_key=True)

    study_id = Column(Integer, ForeignKey('study.id'))
    study = relationship("Study", backref=backref("study_versions"))

    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
  