from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(45), nullable=True)
    type = Column(String(45), nullable=True)

    criterions = relationship("CriterionHasTag", back_populates="tag")
