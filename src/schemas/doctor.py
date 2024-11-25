from typing import Optional

from pydantic import BaseModel, EmailStr


class DoctorBase(BaseModel):
    """
    Base schema for the Doctor model.

    Attributes
    ----------
    email : str
        Email address of the doctor.
    name : Optional[str], optional
        Name of the doctor.
    """

    email: EmailStr
    name: Optional[str] = None


class DoctorCreate(DoctorBase):
    """
    Schema for creating a Doctor instance.

    Attributes
    ----------
    password : str
        Password for the doctor's account.
    """

    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "doctor@example.com",
                "name": "Dr. John Doe",
                "password": "securepassword123",
            }
        }


class DoctorUpdate(BaseModel):
    """
    Schema for updating a Doctor instance.

    Attributes
    ----------
    name : Optional[str], optional
        Updated name of the doctor.
    password : Optional[str], optional
        Updated password for the doctor.
    """

    name: Optional[str] = None
    password: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Dr. Jane Doe",
                "password": "newsecurepassword456",
            }
        }


class DoctorResponse(DoctorBase):
    """
    Schema for the Doctor response.
    """

    class Config:
        json_schema_extra = {
            "example": {
                "email": "doctor@example.com",
                "name": "Dr. John Doe",
            }
        }
