from sqlalchemy import ForeignKey, Integer, DateTime, Boolean, JSON, String
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class StudyHasPatient(Base):
    __tablename__ = 'study_has_patient'
    study_id = mapped_column(Integer, ForeignKey('study.id'), primary_key=True)
    patient_id = mapped_column(String, primary_key=True)
    data = mapped_column(JSON, nullable=False)
    source_id = mapped_column(String, nullable=False, primary_key=True)
    study = relationship("Study", back_populates="patients")

    def __str__(self):
        return f"StudyHasPatient(study_id={self.study_id}, patient_id={self.patient_id}, data={self.data}, source_id{self.source_id})"

