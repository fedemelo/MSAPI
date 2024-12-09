from os import path

from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.config.db_config import get_db
from src.schemas.image import FullImageResponse, ImageCreate, ImageResponse, ImageUpdate
from src.services.image import create_image, delete_image
from src.services.image import (
    delete_images_by_patient as delete_images_by_patient_service,
)
from src.services.image import (
    get_image,
    get_images,
    get_images_by_patient,
    update_image,
)

router = APIRouter(
    prefix="/images",
    tags=["Images"],
    responses={404: {"detail": "Not found"}},
)


@router.get(
    "/{image_id}",
    response_model=FullImageResponse,
    status_code=status.HTTP_200_OK,
)
def read_image(
    image_id: str,
    db: Session = Depends(get_db),
) -> ImageResponse:
    """
    Retrieve an image by ID.

    Attributes
    ----------
    image_id : str
        The image's ID.
    db : Session
        The database session.

    Returns
    -------
    ImageResponse
        The image.
    """
    db_image = get_image(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image


@router.get(
    "/file/{image_id}",
    response_class=FileResponse,
)
def get_image_file(image_id: str, db: Session = Depends(get_db)):
    """
    Serve an image file based on its ID.

    Parameters
    ----------
    image_id : str
        The image ID.
    db : Session
        The database session.

    Returns
    -------
    FileResponse
        The image file.
    """
    image = get_image(db, image_id)
    if not image or not path.exists(image.file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image.file_path)


@router.get(
    "/",
    response_model=list[ImageResponse],
    status_code=status.HTTP_200_OK,
)
def read_many_images(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[ImageResponse]:
    """
    Retrieve a list of images.

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
    list[ImageResponse]
        The images.
    """
    return get_images(db, skip, limit)


@router.get(
    "/patient/{patient_cedula}",
    response_model=list[ImageResponse],
    status_code=status.HTTP_200_OK,
)
def read_images_by_patient(
    patient_cedula: int,
    db: Session = Depends(get_db),
) -> list[ImageResponse]:
    """
    Retrieve a list of images for a patient.

    Attributes
    ----------
    db : Session
        The database session.
    patient_cedula : int
        The patient's cedula.

    Returns
    -------
    list[ImageResponse]
        The images.
    """
    return get_images_by_patient(db, patient_cedula)


@router.post(
    "/",
    response_model=ImageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_image(
    name: str = Body(...),
    patient_cedula: int = Body(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> ImageResponse:
    """
    Create a new image.

    Attributes
    ----------
    name : str
        The image's name.
    patient_cedula : int
        The patient's cedula.
    file : UploadFile
        The image file.
    db : Session
        The database session.

    Returns
    -------
    ImageResponse
        The image.
    """
    image_data = ImageCreate(name=name, patient_cedula=patient_cedula)
    return create_image(db, image_data, file)


@router.put(
    "/{image_id}",
    response_model=ImageResponse,
    status_code=status.HTTP_200_OK,
)
def update_existing_image(
    image_id: str,
    image: ImageUpdate = Body(...),
    db: Session = Depends(get_db),
) -> ImageResponse:
    """
    Update an image's details.

    Attributes
    ----------
    image_id : str
        The image's ID.
    image : ImageUpdate
        The image data.

    Returns
    -------
    ImageResponse
        The updated image.
    """
    return update_image(db, image_id, image)


@router.delete(
    "/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_image(
    image_id: str,
    db: Session = Depends(get_db),
) -> None:
    """
    Delete an image by ID.

    Attributes
    ----------
    image_id : str
        The image's ID.
    db : Session
        The database session.
    """
    delete_image(db, image_id)


@router.delete(
    "/patient/{patient_cedula}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_images_and_predictions_by_patient(
    patient_cedula: int,
    db: Session = Depends(get_db),
) -> None:
    """
    Delete all images for a patient.

    Attributes
    ----------
    patient_cedula : int
        The patient's cedula.
    db : Session
        The database session.
    """
    delete_images_by_patient_service(db, patient_cedula)
