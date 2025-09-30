from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class Tag(Base):
    __tablename__ = 'tag'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    code = mapped_column(String, nullable=True)
    type = mapped_column(String, nullable=True)

    criterions = relationship("CriterionHasTag", back_populates="tag")
