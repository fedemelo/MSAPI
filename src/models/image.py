from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.config.db_config import Base


class Image(Base):
    """
    Model for the images table.

    Attributes
    ----------
    id : UUID
        Unique identifier for the image, primary key.
    name : str
        Name of the image.
    file_path : str
        Path to the stored image file.
    patient_cedula : int
        Foreign key referencing the patient associated with the image.

    patient : Patient
        Relationship with the patients table.
    predictions : List[Prediction]
        Relationship with the predictions table.
    """

    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    patient_cedula = Column(
        Integer, ForeignKey("patients.cedula", ondelete="CASCADE"), nullable=False
    )

    patient = relationship("Patient", back_populates="images")
    predictions = relationship("Prediction", back_populates="image")
