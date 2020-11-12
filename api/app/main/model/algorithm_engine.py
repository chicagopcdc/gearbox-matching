from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt


class StudyAlgorithmEngine(Base):
    __tablename__ = 'study_algorithm_engine'
    study_id = Column(Integer, ForeignKey('study.id'), primary_key=True)
    study_version_id = Column(Integer, ForeignKey('study_version.id'), primary_key=True)
    algorithm_engine_id = Column(Integer, ForeignKey('algorithm_engine.id'), primary_key=True)

    start_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

    study_version = relationship("StudyVersion", back_populates="algorithm_engines")
    algorithm_engine = relationship("AlgorithmEngine", back_populates="study_versions")   


class AlgorithmEngine(Base):
    __tablename__ = 'algorithm_engine'
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String(45), nullable=True)
    name = Column(String(45), nullable=True)
    link = Column(String(256), nullable=True)
    description = Column(String(512), nullable=True)
    function = Column(String(512), nullable=True)
    type = Column(String(45), nullable=True)

    study_versions = relationship("StudyAlgorithmEngine", back_populates="algorithm_engine")   
