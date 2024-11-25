from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.config.db_config import get_db
from src.schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from src.services.patient import (
    create_patient,
    delete_patient,
    get_patient,
    get_patients,
    get_patients_by_doctor,
    update_patient,
)

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
    responses={404: {"detail": "Not found"}},
)


@router.get(
    "/{cedula}",
    response_model=PatientResponse,
    status_code=status.HTTP_200_OK,
)
def read_patient(cedula: int, db: Session = Depends(get_db)):
    """
    Retrieve a patient by cedula.
    """
    db_patient = get_patient(db, cedula)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient


@router.get(
    "/",
    response_model=list[PatientResponse],
    status_code=status.HTTP_200_OK,
)
def read_many_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of patients.
    """
    return get_patients(db, skip, limit)


@router.get(
    "/doctor/{doctor_email}",
    response_model=list[PatientResponse],
    status_code=status.HTTP_200_OK,
)
def read_many_patients_by_doctor(
    doctor_email: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retrieve a list of patients by doctor email.
    """
    return get_patients_by_doctor(db, doctor_email, skip, limit)


@router.post(
    "/",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_patient(
    patient: PatientCreate = Body(...), db: Session = Depends(get_db)
):
    """
    Create a new patient.
    """
    try:
        return create_patient(db, patient)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Patient with this cedula already exists"
        )


@router.put(
    "/{cedula}",
    response_model=PatientResponse,
    status_code=status.HTTP_200_OK,
)
def update_existing_patient(
    cedula: int, patient: PatientUpdate = Body(...), db: Session = Depends(get_db)
):
    """
    Update a patient's details.
    """
    try:
        db_patient = update_patient(db, cedula, patient)
        if not db_patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return db_patient
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{cedula}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_patient(cedula: int, db: Session = Depends(get_db)):
    """
    Delete a patient by cedula.
    """
    db_patient = get_patient(db, cedula)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    delete_patient(db, cedula)
