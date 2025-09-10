from sqlalchemy import Integer, String, DateTime, Boolean, UniqueConstraint,ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base 


class StudyExternalId(Base):
    __tablename__ = "study_external_id"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    study_id = mapped_column(Integer, ForeignKey('study.id'))
    ext_id = mapped_column(String, nullable=True)
    source = mapped_column(String, nullable=True)
    source_url = mapped_column(String, nullable=True)
    active = mapped_column(Boolean, nullable=True)
    create_date = mapped_column(DateTime, nullable=True)

    UniqueConstraint(ext_id, name='study_ext_id_uix')

    study = relationship("Study", back_populates="ext_ids")
