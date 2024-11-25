from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.schemas.prediction import PredictionResponse


class ImageBase(BaseModel):
    """
    Base schema for the Image model.

    Attributes
    ----------
    id : UUID
        Unique identifier for the image.
    name : Optional[str], optional
        Name of the image.
    """

    id: UUID
    name: Optional[str] = None


class ImageCreate(BaseModel):
    """
    Schema for creating an Image instance.

    Attributes
    ----------
    name : str
        Name of the image.
    patient_cedula : int
        Unique identification number for the patient associated with the image.
    """

    name: str
    patient_cedula: int

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Dermoscopic Image",
                "patient_cedula": 123456,
            }
        }


class ImageUpdate(BaseModel):
    """
    Schema for updating an Image instance.

    Attributes
    ----------
    name : Optional[str], optional
        Updated name of the image.
    patient_cedula : Optional[int], optional
        Updated identification number for the patient associated with the image.
    """

    name: Optional[str] = None
    patient_cedula: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Dermoscopic Image",
            }
        }


class ImageResponse(ImageBase):
    """
    Schema for the Image response.

    Attributes
    ----------
    file_path : str
        File path for the stored image.
    """

    name: str
    file_path: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Dermoscopic Image",
                "file_path": "/data/images/patient_123/image_550e8400.jpg",
            }
        }


class FullImageResponse(ImageBase):
    """
    Schema for the Image response.

    Attributes
    ----------
    file_path : str
        File path for the stored image.
    """

    name: str
    file_path: str
    predictions: list[PredictionResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Dermoscopic Image",
                "file_path": "/data/images/patient_123/image_550e8400.jpg",
                "predictions": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "Melanoma",
                        "confidence": 0.85,
                    },
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "Benign",
                        "confidence": 0.15,
                    },
                ],
            }
        }
