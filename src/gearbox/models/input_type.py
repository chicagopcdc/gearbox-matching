from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class InputType(Base):
    __tablename__ = 'input_type'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    data_type = mapped_column(String)
    render_type = mapped_column(String)
    create_date = mapped_column(DateTime, nullable=True)

    criterions = relationship("Criterion", back_populates="input_type", lazy='joined')
