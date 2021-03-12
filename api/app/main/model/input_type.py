from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class InputType(Base):
    __tablename__ = 'input_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_type = Column(String, nullable=True)
    render_type = Column(String, nullable=True)
    name = Column(String, nullable=True)

    values = relationship("InputTypeHasValue", back_populates="input_type")
