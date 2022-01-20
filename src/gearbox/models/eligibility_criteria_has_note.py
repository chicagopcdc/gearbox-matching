from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import relationship

from .base_class import Base


class EligibilityCriteriaHasNote(Base):
    __tablename__ = 'eligibility_criteria_has_note'
    eligibility_criteria_id = Column(Integer, ForeignKey('eligibility_criteria.id'), primary_key=True)
    note_id = Column(Integer, ForeignKey('note.id'), primary_key=True)

    eligibility_criteria = relationship("EligibilityCriteria", back_populates="notes")
    note = relationship("Note", back_populates="eligibility_criterias")
