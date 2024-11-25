from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.db_config import get_db
from src.schemas.doctor import DoctorCreate, DoctorResponse, DoctorUpdate
from src.services.doctor import (
    create_doctor,
    delete_doctor,
    get_doctor,
    get_doctors,
    update_doctor,
)

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
    responses={404: {"detail": "Not found"}},
)


@router.get("/{email}", response_model=DoctorResponse, status_code=status.HTTP_200_OK)
def read_doctor(email: str, db: Session = Depends(get_db)):
    """
    Retrieve a doctor by email.
    """
    db_doctor = get_doctor(db, email)
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor


@router.get("/", response_model=list[DoctorResponse], status_code=status.HTTP_200_OK)
def read_many_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of doctors.
    """
    return get_doctors(db, skip, limit)


@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_new_doctor(doctor: DoctorCreate = Body(...), db: Session = Depends(get_db)):
    """
    Create a new doctor.
    """
    return create_doctor(db, doctor)


@router.put("/{email}", response_model=DoctorResponse, status_code=status.HTTP_200_OK)
def update_existing_doctor(
    email: str, doctor: DoctorUpdate = Body(...), db: Session = Depends(get_db)
):
    """
    Update a doctor's details.
    """
    return update_doctor(db, email, doctor)


@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_doctor(email: str, db: Session = Depends(get_db)):
    """
    Delete a doctor by email.
    """
    delete_doctor(db, email)
