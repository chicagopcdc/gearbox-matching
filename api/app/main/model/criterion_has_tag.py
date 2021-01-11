from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt

class CriterionHasTag(Base):
    __tablename__ = 'criterion_has_tag'
    criterion_id = Column(Integer, ForeignKey('criterion.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)

    criterion = relationship("Criterion", back_populates="tags")
    tag = relationship("Tag", back_populates="criterions")
