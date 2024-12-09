from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.config.db_config import get_db
from src.config.settings import SETTINGS
from src.models.doctor import Doctor
from src.schemas.doctor import DoctorCreate, DoctorUpdate

ALGORITHM = "HS256"
INVALID_TOKEN: str = "Invalid token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/{SETTINGS.API_VERSION}/doctors/login")


def get_current_doctor(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Validate and return the current authenticated doctor.
    """
    try:
        payload = jwt.decode(token, SETTINGS.SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail=INVALID_TOKEN)
        doctor = get_doctor(db, email)
        if doctor is None:
            raise HTTPException(status_code=401, detail=INVALID_TOKEN)
        return doctor
    except JWTError:
        raise HTTPException(status_code=401, detail=INVALID_TOKEN)


def get_doctor(
    db: Session,
    email: str,
) -> Doctor:
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


def get_doctors(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Doctor]:
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


def authenticate_doctor(
    db: Session,
    email: str,
    password: str,
) -> str | None:
    """
    Authenticate a doctor by email and password.

    Parameters
    ----------
    db : Session
        Database session.
    email : str
        Doctor's email.
    password : str
        Doctor's plain text password.

    Returns
    -------
    str
        JWT token if authentication is successful.
    """

    db_doctor = get_doctor(db, email)
    if not db_doctor or not _get_pwd_context().verify(
        password,
        db_doctor.password,
    ):
        return None

    access_token = jwt.encode(
        {"sub": email},
        SETTINGS.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return access_token


def create_doctor(
    db: Session,
    doctor: DoctorCreate,
) -> Doctor:
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
    doctor_data = doctor.model_dump(exclude_none=True)
    doctor_data["password"] = _get_pwd_context().hash(doctor.password)
    db_doctor = Doctor(**doctor_data)
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def update_doctor(
    db: Session,
    email: str,
    doctor: DoctorUpdate,
) -> Doctor:
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


def delete_doctor(
    db: Session,
    email: str,
) -> None:
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


def _get_pwd_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")
