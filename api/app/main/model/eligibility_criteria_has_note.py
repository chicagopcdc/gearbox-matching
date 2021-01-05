from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt

class EligibilityCriteriaHasNote(Base):
    __tablename__ = 'eligibility_criteria_has_note'
    eligibility_criteria_id = Column(Integer, ForeignKey('eligibility_criteria.id'), primary_key=True)
    note_id = Column(Integer, ForeignKey('note.id'), primary_key=True)
