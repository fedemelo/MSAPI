from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from src.config.db_config import get_db
from src.schemas.prediction import PredictionCreate, PredictionResponse
from src.services.prediction import (
    create_prediction,
    delete_prediction,
    get_prediction,
    get_predictions,
    get_predictions_by_image_id,
)

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
    responses={404: {"detail": "Not found"}},
)


@router.get(
    "/{prediction_id}",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
)
def read_prediction(
    prediction_id: str,
    db: Session = Depends(get_db),
):
    """
    Retrieve a prediction by ID.

    Attributes
    ----------
    prediction_id : str
        The prediction's ID.
    db : Session
        The database session.
    """
    db_prediction = get_prediction(db, prediction_id)
    if not db_prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return db_prediction


@router.get(
    "/",
    response_model=list[PredictionResponse],
    status_code=status.HTTP_200_OK,
)
def read_many_predictions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[PredictionResponse]:
    """
    Retrieve a list of predictions.

    Attributes
    ----------
    skip : int
        The number of predictions to skip.
    limit : int
        The number of predictions to return.
    db : Session
        The database session.

    Returns
    -------
    list[PredictionResponse]
        The predictions.
    """
    return get_predictions(db, skip, limit)


@router.get(
    "/image/{image_id}",
    response_model=list[PredictionResponse],
    status_code=status.HTTP_200_OK,
)
def read_predictions_by_image_id(
    image_id: str,
    db: Session = Depends(get_db),
) -> list[PredictionResponse]:
    """
    Retrieve a list of predictions for a given image.

    Attributes
    ----------
    image_id : str
        The image's ID.
    db : Session
        The database session.

    Returns
    -------
    list[PredictionResponse]
        The predictions.
    """
    return get_predictions_by_image_id(db, image_id)


@router.post(
    "/",
    response_model=PredictionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_prediction(
    image_id: str = Body(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> PredictionResponse:
    """
    Create a new prediction.

    Attributes
    ----------
    image_id : str
        The image's ID.
    file : UploadFile
        The prediction file.
    db : Session
        The database session.

    Returns
    -------
    PredictionResponse
        The prediction.
    """
    prediction_data = PredictionCreate(image_id=image_id)
    return create_prediction(db, prediction_data, file)


@router.delete(
    "/{prediction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_prediction(
    prediction_id: str,
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a prediction by ID.

    Attributes
    ----------
    prediction_id : str
        The prediction's ID.
    db : Session
        The database session.
    """
    delete_prediction(db, prediction_id)
