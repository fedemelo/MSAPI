from typing import Optional

from pydantic import BaseModel


class PatientBase(BaseModel):
    """
    Base schema for the Patient model.

    Attributes
    ----------
    cedula : int
        Unique identification number for the patient.
        Ideally a Colombian cedula number.
    name : Optional[str], optional
        Name of the patient.
    """

    cedula: int
    name: Optional[str] = None


class PatientCreate(PatientBase):
    """
    Schema for creating a Patient instance.

    Attributes
    ----------
    doctor_email : str
        Email address of the doctor associated with the patient.
    """

    doctor_email: str

    class Config:
        json_schema_extra = {
            "example": {
                "cedula": 123456789,
                "name": "John Smith",
                "doctor_email": "doctor@example.com",
            }
        }


class PatientUpdate(BaseModel):
    """
    Schema for updating a Patient instance.

    Attributes
    ----------
    name : Optional[str], optional
        Updated name of the patient.
    doctor_email : Optional[str], optional
        Updated email address of the doctor associated with the patient.
    """

    name: Optional[str] = None
    doctor_email: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jane Smith",
            }
        }


class PatientResponse(PatientBase):
    """
    Schema for the Patient response.
    """

    class Config:
        json_schema_extra = {
            "example": {
                "cedula": 123456789,
                "name": "John Smith",
            }
        }
