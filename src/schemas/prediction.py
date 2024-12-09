from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PredictionBase(BaseModel):
    """
    Base schema for the Prediction model.

    Attributes
    ----------
    id : UUID
        Unique identifier for the prediction.
    timestamp : datetime
        Time when the prediction was made.
    """

    id: UUID
    timestamp: datetime


class PredictionCreate(BaseModel):
    """
    Schema for creating a Prediction instance.

    Attributes
    ----------
    image_id : UUID
        Foreign key referencing the image associated with the prediction.
    """

    image_id: UUID

    class Config:
        json_schema_extra = {
            "example": {
                "image_id": "550e8400-e29b-41d4-a716-446655440000",
            }
        }


class PredictionResponse(PredictionBase):
    """
    Schema for the Prediction response.
    """

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "timestamp": "2024-11-24T12:34:56",
            }
        }
