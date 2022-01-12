from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref

from .base_class import Base


class Criterion(Base):
    __tablename__ = 'criterion'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, nullable=True)
    display_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)


    ontology_code_id = Column(Integer, ForeignKey('ontology_code.id'), nullable=True)

    input_type_id = Column(Integer, ForeignKey('input_type.id'), nullable=True)
    input_type = relationship("InputType", backref=backref("criterions"))
    
