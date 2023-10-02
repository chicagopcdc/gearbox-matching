from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship

from .base_class import Base


class SiteHasStudy(Base):
    __tablename__ = 'site_has_study'
    study_id = Column(Integer, ForeignKey('study.id'), primary_key=True)
    patient_id = Column(Integer, primary_key=True)
    data = Column(JSON, nullable=False)

    study = relationship("Study", back_populates="sites")


