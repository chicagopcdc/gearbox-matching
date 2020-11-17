from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt

class Treatment(Base):
    __tablename__ = 'treatment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    level_code = Column(String(45), nullable=True)
    level_display = Column(String(128), nullable=True)
    description = Column(String(512), nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
