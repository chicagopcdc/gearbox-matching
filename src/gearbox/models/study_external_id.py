from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint,ForeignKey
from sqlalchemy.orm import relationship

from .base_class import Base 


class StudyExternalId(Base):
    __tablename__ = "study_external_id"

    id = Column(Integer, primary_key=True, autoincrement=True)
    study_id = Column(Integer, ForeignKey('study.id'))
    ext_id = Column(String, nullable=True)
    source = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    active = Column(Boolean, nullable=True)

    UniqueConstraint(study_id, ext_id, name='study_ext_id_uix')

    study = relationship("Study", back_populates="ext_ids")