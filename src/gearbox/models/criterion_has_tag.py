from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import relationship

from .base_class import Base


class CriterionHasTag(Base):
    __tablename__ = 'criterion_has_tag'
    criterion_id = Column(Integer, ForeignKey('criterion.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)

    criterion = relationship("Criterion", back_populates="tags")
    tag = relationship("Tag", back_populates="criterions", lazy="joined")
