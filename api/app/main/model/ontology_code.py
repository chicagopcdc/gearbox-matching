from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt

class OntologyCode(Base):
    __tablename__ = 'ontology_code'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ontology_url = Column(String(45), nullable=True)
    name = Column(String(45), nullable=True)
    code = Column(String(45), nullable=True)
    value = Column(String(45), nullable=True)
    version = Column(String(45), nullable=True)
