from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt

class ArmTreatment(Base):
    __tablename__ = 'arm_treatment'
    arm_id = Column(Integer, ForeignKey('arm.id'), primary_key=True)
    treatment_id = Column(Integer, ForeignKey('treatment.id'), primary_key=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

#    arm = relationship("Arm", back_populates="arm_treament")
#    treatment = relationship("Treatment", back_populates="arm_treament")
