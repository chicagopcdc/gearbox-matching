from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import relationship, backref

from .base_class import Base

class EligibilityCriteriaHasNote(Base):
    __tablename__ = 'eligibility_criteria_has_note'
    
    eligibility_criteria_id = Column(Integer, ForeignKey('eligibility_criteria.id'), primary_key=True)
    eligibility_criteria = relationship("EligibilityCriteria", backref=backref("notes"))

    note_id = Column(Integer, ForeignKey('note.id'), primary_key=True)
    note = relationship("Note", backref=backref("eligibility_criterias"))
