from sqlalchemy import ForeignKey, Integer, DateTime, Text, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from .base_class import Base


class SavedInput(Base):
    __tablename__ = 'saved_input'
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, nullable=False)
    name = mapped_column(String)
    patient_id = mapped_column(Integer, nullable=True)
    create_date = mapped_column(DateTime, nullable=False)
    update_date = mapped_column(DateTime, nullable=False)
    data = mapped_column(JSONB(astext_type=Text()), nullable=False)
    

