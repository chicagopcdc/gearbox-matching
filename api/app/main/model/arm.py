from sqlalchemy import Column, Integer, String, DateTime, Boolean

from . import Base
from app.main import DbSession

class Arm(Base):
    __tablename__ = "arm"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)
    study_id = Column(Integer, nullable=False)
    code = Column(String(45), nullable=True)
    create_date = Column(DateTime, nullable=False)
    active = Column(Boolean, nullable=False, default=True)


    
