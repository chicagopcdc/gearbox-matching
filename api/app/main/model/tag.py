from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, nullable=True)
    type = Column(String, nullable=True)

    criterions = relationship("CriterionHasTag", back_populates="tag")
