from sqlalchemy import Column, Integer, String

from . import Base


class OntologyCode(Base):
    __tablename__ = 'ontology_code'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ontology_url = Column(String, nullable=True)
    name = Column(String, nullable=True)
    code = Column(String, nullable=True)
    value = Column(String, nullable=True)
    version = Column(String, nullable=True)

