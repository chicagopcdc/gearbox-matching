from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt


class StudyVersion(Base):
    __tablename__ = "study_version"

    id = Column(Integer, primary_key=True)
    study_id = Column(Integer, ForeignKey('study.id'), primary_key=True) 
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
  
    algorithm_engines = relationship("StudyAlgorithmEngine", back_populates="study_version")
