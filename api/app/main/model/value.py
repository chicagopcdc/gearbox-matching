from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from . import Base


class Value(Base):
    __tablename__ = 'value'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, nullable=True)
    type = Column(String, nullable=True)
    value_string = Column(String, nullable=True)
    upper_threshold = Column(Float, nullable=True)
    lower_threshold = Column(Float, nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
    value_list = Column(String, nullable=True)
    value_bool = Column(String, nullable=True)
    upper_modifier = Column(String, nullable=True)
    lower_modifier = Column(String, nullable=True)

    el_criteria_has_criterions = relationship("ElCriteriaHasCriterion", back_populates="value")
    criteria = relationship("InputTypeHasValue", back_populates="value")
