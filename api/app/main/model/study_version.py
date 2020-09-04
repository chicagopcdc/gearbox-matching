from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession
from app.main.model.algorithm_engine import StudyAlgorithmEngine

# , flask_bcrypt


class StudyVersion(Base):
    __tablename__ = "study_version"

    #DEBUG
    #id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, primary_key=True)
    study_id = Column(Integer, ForeignKey('study.id'), primary_key=True) 
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

    #DEBUG
    algorithm_engines = relationship("StudyAlgorithmEngine", back_populates="study_version")
    #algorithm_engines = relationship("StudyAlgorithmEngine", back_populates="study_version", cascade="all, delete-orphan")

    study = relationship("Study", back_populates="study_versions")
