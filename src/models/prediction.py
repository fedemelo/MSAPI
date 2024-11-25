from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.config.db_config import Base


class Prediction(Base):
    """
    Model for the predictions table.

    Attributes
    ----------
    id : UUID
        Unique identifier for the prediction, primary key.
    file_path : str
        File path associated with the prediction.
    timestamp : datetime
        Time when the prediction was made.
    image_id : UUID
        Foreign key referencing the image associated with the prediction.

    image : Image
        Relationship with the images table.
    """

    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=True), primary_key=True)
    file_path = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    image_id = Column(
        UUID(as_uuid=True), ForeignKey("images.id", ondelete="CASCADE"), nullable=False
    )

    image = relationship("Image", back_populates="predictions")
