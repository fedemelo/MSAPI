from sqlalchemy.orm import Session

from src.models.doctor import Doctor
from src.schemas.doctor import DoctorCreate, DoctorUpdate


def get_doctor(db: Session, email: str) -> Doctor:
    """
    Get a doctor by email.

    Parameters
    ----------
    db : Session
        Database session.
    email : str
        Doctor's email.

    Returns
    -------
    Doctor
        Doctor record.
    """
    return db.query(Doctor).filter(Doctor.email == email).first()


def get_doctors(db: Session, skip: int = 0, limit: int = 100) -> list[Doctor]:
    """
    Get many doctors.

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
    list[Doctor]
        List of doctor records.
    """
    return db.query(Doctor).offset(skip).limit(limit).all()


def create_doctor(db: Session, doctor: DoctorCreate) -> Doctor:
    """
    Create a new doctor.

    Parameters
    ----------
    db : Session
        Database session.
    doctor : DoctorCreate
        Doctor data.

    Returns
    -------
    Doctor
        Newly created doctor.
    """
    db_doctor = Doctor(**doctor.model_dump(exclude_none=True))
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def update_doctor(db: Session, email: str, doctor: DoctorUpdate) -> Doctor:
    """
    Update a doctor.

    Parameters
    ----------
    db : Session
        Database session.
    email : str
        Doctor's email.
    doctor : DoctorUpdate
        Updated doctor data.

    Returns
    -------
    Doctor
        Updated doctor record.
    """
    db.query(Doctor).filter(Doctor.email == email).update(
        doctor.model_dump(exclude_none=True)
    )
    db.commit()
    return get_doctor(db, email)


def delete_doctor(db: Session, email: str) -> None:
    """
    Delete a doctor.

    Parameters
    ----------
    db : Session
        Database session.
    email : str
        Doctor's email.
    """
    db.query(Doctor).filter(Doctor.email == email).delete()
    db.commit()
