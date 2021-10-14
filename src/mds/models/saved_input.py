from sqlalchemy import ForeignKey, Column, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB

from .base_class import Base


class SavedInput(Base):
    __tablename__ = 'saved_input'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    patient_id = Column(Integer, nullable=True)
    create_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=False)
    data = Column(JSONB(astext_type=Text()), nullable=False)
    

