from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class Note(Base):
    __tablename__ = 'note'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    value = mapped_column(String, nullable=True)

    eligibility_criterias = relationship("EligibilityCriteriaHasNote", back_populates="note")
