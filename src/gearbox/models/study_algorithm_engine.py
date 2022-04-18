from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship

from .base_class import Base


class StudyAlgorithmEngine(Base):
    __tablename__ = 'study_algorithm_engine'
    id = Column(Integer, primary_key=True, autoincrement=True)
    study_version_id = Column(Integer, ForeignKey('study_version.id'))
#    algorithm_engine_id = Column(Integer, ForeignKey('algorithm_engine.id'), primary_key=True)
    start_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

    algorithm_engine = relationship("AlgorithmEngine", back_populates="study_algo_engine")
    study_version = relationship("StudyVersion", back_populates="algorithm_engines")
