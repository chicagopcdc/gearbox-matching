from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class CriterionHasTag(Base):
    __tablename__ = 'criterion_has_tag'
    criterion_id = mapped_column(Integer, ForeignKey('criterion.id'), primary_key=True)
    tag_id = mapped_column(Integer, ForeignKey('tag.id'), primary_key=True)

    criterion = relationship("Criterion", back_populates="tags")
    tag = relationship("Tag", back_populates="criterions", lazy="joined",cascade="save-update, merge, delete, delete-orphan", single_parent=True)
