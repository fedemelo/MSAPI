import os
import shutil
from datetime import datetime
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.image import Image
from src.models.prediction import Prediction
from src.schemas.prediction import PredictionCreate

BASE_PREDICTION_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "images",
)


def get_prediction(
    db: Session,
    prediction_id: str,
) -> Prediction:
    """
    Get a prediction by ID.

    Attributes
    ----------
    db : Session
        The database session.
    prediction_id : str
        The prediction's ID.

    Returns
    -------
    Prediction
        The prediction.
    """
    return db.query(Prediction).filter(Prediction.id == prediction_id).first()


def get_predictions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Prediction]:
    """
    Get many predictions.

    Attributes
    ----------
    db : Session
        The database session.
    skip : int
        The number of predictions to skip.
    limit : int
        The number of predictions to return

    Returns
    -------
    list[Prediction]
        The predictions.
    """
    return db.query(Prediction).offset(skip).limit(limit).all()


def get_predictions_by_image_id(
    db: Session,
    image_id: str,
) -> list[Prediction]:
    """
    Get all predictions for a given image.

    Attributes
    ----------
    db : Session
        The database session.
    image_id : str
        The image's ID.

    Returns
    -------
    list[Prediction]
        The predictions.
    """
    return db.query(Prediction).filter(Prediction.image_id == image_id).all()


def create_prediction(
    db: Session,
    prediction: PredictionCreate,
    uploaded_file: UploadFile,
) -> Prediction:
    """
    Create a new prediction and save the file to local storage.

    Attributes
    ----------
    db : Session
        The database session.
    prediction : PredictionCreate
        The prediction data.
    uploaded_file : UploadFile
        The uploaded file.

    Returns
    -------
    Prediction
        The prediction
    """
    image = _get_image_or_raise(db, prediction.image_id)
    patient_dir = _validate_patient_directory(image.patient_cedula)
    prediction_id = uuid4()
    file_path = _save_prediction_file(patient_dir, uploaded_file, prediction_id)
    return _save_prediction_to_database(db, prediction, file_path, prediction_id)


def _get_image_or_raise(
    db: Session,
    image_id: str,
) -> Image:
    """
    Fetch the image from the database or raise an error if not found.

    Attributes
    ----------
    db : Session
        The database session.
    image_id : str
        The image's ID.

    Returns
    -------
    Image
        The image.
    """
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise RuntimeError(f"Image with ID {image_id} not found")
    return image


def _validate_patient_directory(
    patient_cedula: int,
) -> str:
    """
    Validate that the patient directory exists, or raise an error.

    Attributes
    ----------
    patient_cedula : int
        The patient's cedula.

    Returns
    -------
    str
        The patient's directory.
    """
    patient_dir = os.path.join(BASE_PREDICTION_DIR, f"patient_{patient_cedula}")
    if not os.path.exists(patient_dir):
        raise RuntimeError(f"Patient directory not found: {patient_dir}")
    return patient_dir


def _save_prediction_file(
    patient_dir: str,
    uploaded_file: UploadFile,
    prediction_id: uuid4,
) -> str:
    """
    Save the uploaded prediction file to the local filesystem.

    Attributes
    ----------
    patient_dir : str
        The directory where the file will be saved.
    uploaded_file : UploadFile
        The file to save.
    prediction_id : str
        The prediction's ID.

    Returns
    -------
    str
        The path to the saved file.
    """
    file_name = (
        f"prediction_{prediction_id}{os.path.splitext(uploaded_file.filename)[-1]}"
    )
    file_path = os.path.join(patient_dir, file_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
    except Exception as e:
        raise RuntimeError(f"Failed to save the prediction file: {e}")

    return file_path


def _save_prediction_to_database(
    db: Session,
    prediction: PredictionCreate,
    file_path: str,
    prediction_id: uuid4,
) -> Prediction:
    """
    Save the prediction record to the database.

    Attributes
    ----------
    db : Session
        The database session.
    prediction : PredictionCreate
        The prediction data.
    file_path : str
        The path to the saved prediction file.
    prediction_id : str
        The prediction's ID.

    Returns
    -------
    Prediction
        The saved prediction.
    """
    try:
        db_prediction = Prediction(
            id=prediction_id,
            file_path=file_path,
            timestamp=datetime.now(),
            image_id=prediction.image_id,
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        return db_prediction
    except SQLAlchemyError as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise RuntimeError(f"Failed to save the prediction in the database: {e}")


def delete_prediction(
    db: Session,
    prediction_id: str,
) -> None:
    """
    Delete a prediction and its file from local storage.

    Attributes
    ----------
    db : Session
        The database session.
    prediction_id : str
        The prediction's ID.
    """
    db_prediction = get_prediction(db, prediction_id)
    if db_prediction:
        try:
            if os.path.exists(db_prediction.file_path):
                os.remove(db_prediction.file_path)

            db.query(Prediction).filter(Prediction.id == prediction_id).delete()
            db.commit()
        except Exception as e:
            db.rollback()
            raise RuntimeError(f"Failed to delete the prediction: {e}")


def delete_predictions_by_image_id(
    db: Session,
    image_id: str,
) -> None:
    """
    Delete all predictions associated with an image.

    Attributes
    ----------
    db : Session
        The database session.
    image_id : str
        The image's ID.
    """
    db_predictions = get_predictions_by_image_id(db, image_id)
    for db_prediction in db_predictions:
        delete_prediction(db, db_prediction.id)
