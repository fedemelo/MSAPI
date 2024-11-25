import os
import shutil
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.image import Image
from src.schemas.image import ImageCreate, ImageUpdate
from src.services.prediction import delete_predictions_by_image_id

BASE_IMAGE_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "images",
)


def get_image(
    db: Session,
    image_id: str,
) -> Image:
    """
    Get an image by ID.

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
    return db.query(Image).filter(Image.id == image_id).first()


def get_images(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Image]:
    """
    Get many images.

    Attributes
    ----------
    db : Session
        The database session.
    skip : int
        The number of images to skip.
    limit : int
        The number of images to return

    Returns
    -------
    list[Image]
        The images.
    """
    return db.query(Image).offset(skip).limit(limit).all()


def get_images_by_patient(
    db: Session,
    patient_cedula: int,
) -> list[Image]:
    """
    Get all images for a patient.

    Attributes
    ----------
    db : Session
        The database session.
    patient_cedula : int
        The patient's cedula.

    Returns
    -------
    list[Image]
        The patient's images.
    """
    return db.query(Image).filter(Image.patient_cedula == patient_cedula).all()


def create_image(
    db: Session,
    image: ImageCreate,
    uploaded_file: UploadFile,
) -> Image:
    """
    Create a new image and save the file to local storage and database.

    Attributes
    ----------
    db : Session
        The database session.
    image : ImageCreate
        The image data.
    uploaded_file : UploadFile
        The image file.

    Returns
    -------
    Image
        The created image.
    """
    patient_dir = _create_patient_directory(image.patient_cedula)
    image_id = uuid4()
    file_path = _save_uploaded_file(patient_dir, uploaded_file, image_id)
    return _save_image_to_database(db, image, file_path, image_id)


def _create_patient_directory(
    patient_cedula: str,
) -> str:
    """
    Create a directory for the patient's images if it doesn't exist.

    Attributes
    ----------
    patient_cedula : str
        The patient's cedula.

    Returns
    -------
    str
        The path to the patient
    """
    patient_dir = os.path.join(BASE_IMAGE_DIR, f"patient_{patient_cedula}")
    os.makedirs(patient_dir, exist_ok=True)
    return patient_dir


def _save_uploaded_file(
    patient_dir: str,
    uploaded_file: UploadFile,
    image_id: uuid4,
) -> str:
    """
    Save the uploaded file to the local filesystem.

    Attributes
    ----------
    patient_dir : str
        The directory where the file will be saved.
    uploaded_file : UploadFile
        The file to save.
    image_id : uuid4
        The image's ID.

    Returns
    -------
    str
        The path to the saved file.
    """
    file_name = f"image_{image_id}{os.path.splitext(uploaded_file.filename)[-1]}"
    file_path = os.path.join(patient_dir, file_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
    except Exception as e:
        raise RuntimeError(f"Failed to save the image file: {e}")

    return file_path


def _save_image_to_database(
    db: Session,
    image: ImageCreate,
    file_path: str,
    image_id: uuid4,
) -> Image:
    """
    Save the image record to the database.

    Attributes
    ----------
    db : Session
        The database session.
    image : ImageCreate
        The image data.
    file_path : str
        The path to the saved image file.
    image_id : uuid4
        The image's ID.

    Returns
    -------
    Image
        The saved image.
    """
    try:
        db_image = Image(
            id=image_id,
            name=image.name,
            file_path=file_path,
            patient_cedula=image.patient_cedula,
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image
    except SQLAlchemyError as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise RuntimeError(f"Failed to save the image in the database: {e}")


def update_image(
    db: Session,
    image_id: str,
    image: ImageUpdate,
) -> Image:
    """
    Update an image's metadata in the database.

    Attributes
    ----------
    db : Session
        The database session.
    image_id : str
        The image's ID.
    image : ImageUpdate
        The updated image data.

    Returns
    -------
    Image
        The updated image.
    """
    try:
        db.query(Image).filter(Image.id == image_id).update(
            image.model_dump(exclude_none=True)
        )
        db.commit()
        return get_image(db, image_id)
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Failed to update the image: {e}")


def delete_image(
    db: Session,
    image_id: str,
) -> None:
    """
    Delete an image and its file from local storage.

    Attributes
    ----------
    db : Session
        The database session.
    image_id : str
        The image's ID.
    """
    db_image = get_image(db, image_id)

    if db_image:
        try:
            delete_predictions_by_image_id(db, image_id)

            if os.path.exists(db_image.file_path):
                os.remove(db_image.file_path)

            db.query(Image).filter(Image.id == image_id).delete()
            db.commit()
        except Exception as e:
            db.rollback()
            raise RuntimeError(f"Failed to delete the image: {e}")


def delete_images_by_patient(
    db: Session,
    patient_cedula: int,
) -> None:
    """
    Delete all images for a patient.

    Attributes
    ----------
    db : Session
        The database session.
    patient_cedula : int
        The patient's cedula.
    """
    patient_dir = os.path.join(BASE_IMAGE_DIR, f"patient_{patient_cedula}")

    try:
        if os.path.exists(patient_dir):
            shutil.rmtree(patient_dir)

        db.query(Image).filter(Image.patient_cedula == patient_cedula).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Failed to delete the images: {e}")
