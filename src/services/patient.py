from sqlalchemy.orm import Session

from src.models.doctor import Doctor
from src.models.patient import Patient
from src.schemas.patient import PatientCreate, PatientUpdate


def get_patient(db: Session, cedula: int) -> Patient:
    """
    Get a patient by cedula.

    Parameters
    ----------
    db : Session
        Database session.
    cedula : int
        Patient's cedula.

    Returns
    -------
    Patient
        Patient record.
    """
    return db.query(Patient).filter(Patient.cedula == cedula).first()


def get_patients(db: Session, skip: int = 0, limit: int = 100) -> list[Patient]:
    """
    Get many patients.

    Parameters
    ----------
    db : Session
        Database session.
    skip : int, optional
        Skip records, by default 0.
    limit : int, optional
        Limit of records, by default 100.

    Returns
    -------
    list[Patient]
        List of patient records.
    """
    return db.query(Patient).offset(skip).limit(limit).all()


def get_patients_by_doctor(
    db: Session,
    doctor_email: str,
    skip: int = 0,
    limit: int = 100,
) -> list[Patient]:
    """
    Get many patients by doctor email.

    Parameters
    ----------
    db : Session
        Database session.
    doctor_email : str
        Doctor's email.
    skip : int, optional
        Skip records, by default 0.
    limit : int, optional
        Limit of records, by default 100.

    Returns
    -------
    list[Patient]
        List of patient records.
    """
    return (
        db.query(Patient)
        .filter(Patient.doctor_email == doctor_email)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_patient(db: Session, patient: PatientCreate) -> Patient:
    """
    Create a new patient.

    Parameters
    ----------
    db : Session
        Database session.
    patient : PatientCreate
        Patient data.

    Returns
    -------
    Patient
        Newly created patient.

    Raises
    ------
    ValueError
        If the associated doctor does not exist.
    """
    doctor = db.query(Doctor).filter(Doctor.email == patient.doctor_email).first()
    if not doctor:
        raise ValueError(f"Doctor with email {patient.doctor_email} does not exist.")

    db_patient = Patient(**patient.model_dump(exclude_none=True))
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def update_patient(db: Session, cedula: int, patient: PatientUpdate) -> Patient:
    """
    Update a patient.

    Parameters
    ----------
    db : Session
        Database session.
    cedula : int
        Patient's cedula.
    patient : PatientUpdate
        Updated patient data.

    Returns
    -------
    Patient
        Updated patient record.

    Raises
    ------
    ValueError
        If updating the doctor_email and the new doctor does not exist.
    """
    if patient.doctor_email:
        doctor = db.query(Doctor).filter(Doctor.email == patient.doctor_email).first()
        if not doctor:
            raise ValueError(
                f"Doctor with email {patient.doctor_email} does not exist."
            )

    db.query(Patient).filter(Patient.cedula == cedula).update(
        patient.model_dump(exclude_none=True)
    )
    db.commit()
    return get_patient(db, cedula)


def delete_patient(db: Session, cedula: int) -> None:
    """
    Delete a patient.

    Parameters
    ----------
    db : Session
        Database session.
    cedula : int
        Patient's cedula.
    """
    db.query(Patient).filter(Patient.cedula == cedula).delete()
    db.commit()
