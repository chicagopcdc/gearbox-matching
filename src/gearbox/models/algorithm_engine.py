from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from .base_class import Base

class AlgorithmEngine(Base):
    __tablename__ = 'algorithm_engine'

    id = Column(Integer, primary_key=True, autoincrement=True)
    study_algorithm_engine_id = Column(Integer, ForeignKey('study_algorithm_engine.id'))
    el_criteria_has_criterion_id = Column(Integer, ForeignKey('el_criteria_has_criterion.id'))
    path = Column(String)
    sequence = Column(Integer)

    # study_version = relationship("StudyAlgorithmEngine", back_populates="algorithm_engine")   
    study_algo_engine = relationship("StudyAlgorithmEngine", back_populates="algorithm_engine")   
