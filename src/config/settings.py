import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Settings for the project.

    Attributes:
    -----------
    PROJECT_NAME: str
        The name of the project. By default, "MSAPI".
    DB_NAME: str
        The name of the database. By default, "melanoma_segmentation_db".
    DB_USER: str
        The username for the database.
    DB_PASSWORD: str
        The password for the database.
    DB_HOST: str
        The host in which the database is running.
    DB_PORT: str
        The port in which the database is running.
    """

    PROJECT_NAME: str = "MSAPI"
    DB_NAME: str = "melanoma_segmentation_db"
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    API_VERSION: str = "v1.0"

    class Config:
        case_sensitive = True


SETTINGS = Settings()
