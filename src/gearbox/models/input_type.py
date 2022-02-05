from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .base_class import Base


class InputType(Base):
    __tablename__ = 'input_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_type = Column(String, nullable=True)
    render_type = Column(String, nullable=True)
    create_date = Column(DateTime, nullable=True)

    criterions = relationship("Criterion", back_populates="input_type", lazy='joined')