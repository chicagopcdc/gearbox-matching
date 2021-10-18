from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship, backref

from . import Base


class StudyAlgorithmEngine(Base):
    __tablename__ = 'study_algorithm_engine'
    
    study_version_id = Column(Integer, ForeignKey('study_version.id'), primary_key=True)
    study_version = relationship("StudyVersion", backref=backref("algorithm_engines"))

    algorithm_engine_id = Column(Integer, ForeignKey('algorithm_engine.id'), primary_key=True)
    algorithm_engine = relationship("AlgorithmEngine", backref=backref("study_versions"))


    start_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

