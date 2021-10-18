from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from .db import db


class AlgorithmEngine(db.Model):
    __tablename__ = 'algorithm_engine'

    id = Column(Integer, primary_key=True, autoincrement=True)
    el_criteria_has_criterion_id = Column(Integer, ForeignKey('el_criteria_has_criterion.id'))
    parent_id = Column(Integer)
    parent_path = Column(String)
    operator = Column(String, nullable=True)
