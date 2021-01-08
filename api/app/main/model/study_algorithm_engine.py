from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt


class StudyAlgorithmEngine(Base):
    __tablename__ = 'study_algorithm_engine'
    study_version_id = Column(Integer, ForeignKey('study_version.id'), primary_key=True)
    algorithm_engine_id = Column(Integer, ForeignKey('algorithm_engine.id'), primary_key=True)
    start_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

#    study_version = relationship("StudyVersion", back_populates="algorithm_engines")
#    algorithm_engine = relationship("AlgorithmEngine", back_populates="study_versions")
