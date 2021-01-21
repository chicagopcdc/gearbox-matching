from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Note(Base):
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(45), nullable=True)

    eligibility_criterias = relationship("EligibilityCriteriaHasNote", back_populates="note")
