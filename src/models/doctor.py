from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.config.db_config import Base


class Doctor(Base):
    """
    Model for the doctors table.

    Attributes
    ----------
    email : str
        Email address of the doctor, primary key.
    name : str
        Name of the doctor.
    password : str
        Password for the doctor's account.

    patients : List[Patient]
        Relationship with the patients table.
    """

    __tablename__ = "doctors"

    email = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    password = Column(String, nullable=False)

    patients = relationship("Patient", back_populates="doctor")
