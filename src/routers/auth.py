from fastapi import APIRouter, Depends, status

from models.doctor import Doctor
from src.services.doctor import get_current_doctor

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"detail": "Not found"}},
)


@router.get(
    "/check",
    status_code=status.HTTP_200_OK,
)
def check_auth(
    current_doctor: Doctor = Depends(get_current_doctor),
):
    """
    Check if the user is authenticated.

    Returns
    -------
    dict
        A simple message indicating the user is authenticated.
    """
    return {"message": "User is authenticated"}
