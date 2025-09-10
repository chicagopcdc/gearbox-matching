from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import mapped_column

from .base_class import Base


class OntologyCode(Base):
    __tablename__ = 'ontology_code'
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    ontology_url = mapped_column(String, nullable=True)
    name = mapped_column(String, nullable=True)
    code = mapped_column(String, nullable=True)
    value = mapped_column(String, nullable=True)
    version = mapped_column(String, nullable=True)
    UniqueConstraint(name, code, version, name='ontology_code_uix')

