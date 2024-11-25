from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.config.db_config import Base


class Patient(Base):
    """
    Model for the patients table.

    Attributes
    ----------
    cedula : int
        Unique identification number for the patient, primary key.
    name : str
        Name of the patient.
    doctor_email : str
        Foreign key referencing the doctor associated with the patient.

    doctor : Doctor
        Relationship with the doctors table.
    images : List[Image]
        Relationship with the images table.
    """

    __tablename__ = "patients"

    cedula = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    doctor_email = Column(String, ForeignKey("doctors.email"), nullable=False)

    doctor = relationship("Doctor", back_populates="patients")
    images = relationship("Image", back_populates="patient")
