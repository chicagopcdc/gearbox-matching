from sqlalchemy import ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .base_class import Base

class AlgorithmEngine(Base):
    __tablename__ = 'algorithm_engine'

    id = Column(Integer, primary_key=True, autoincrement=True)
    study_algorithm_engine_id = Column(Integer, ForeignKey('study_algorithm_engine.id'))
    algorithm_engine_version = Column(Integer, nullable=True)
    algorithm_logic = Column(JSONB)
    active = Column(Boolean, nullable=True)

    study_algo_engine = relationship("StudyAlgorithmEngine", back_populates="algorithm_engine")   
