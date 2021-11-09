from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import relationship, backref

from . import Base


class CriterionHasTag(Base):
    __tablename__ = 'criterion_has_tag'


    criterion_id = Column(Integer, ForeignKey('criterion.id'), primary_key=True)
    criterion = relationship("Criterion", backref=backref("tags"))

    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)
    tag = relationship("Tag", backref=backref("criterions"))
