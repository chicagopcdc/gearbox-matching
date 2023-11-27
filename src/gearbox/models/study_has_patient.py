from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean, JSON, String
from sqlalchemy.orm import relationship

from .base_class import Base


class StudyHasPatient(Base):
    __tablename__ = 'study_has_patient'
    study_id = Column(Integer, ForeignKey('study.id'), primary_key=True)
    patient_id = Column(String, primary_key=True)
    data = Column(JSON, nullable=False)
    source_id = Column(String, nullable=False, primary_key=True)
    study = relationship("Study", back_populates="patients")

    def __str__(self):
        return f"StudyHasPatient(study_id={self.study_id}, patient_id={self.patient_id}, data={self.data}, source_id{self.source_id})"

