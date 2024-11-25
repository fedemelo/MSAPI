from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config.settings import SETTINGS

SQLALCHEMY_DATABASE_URL = f"postgresql://{SETTINGS.DB_USER}:{SETTINGS.DB_PASSWORD}@{SETTINGS.DB_HOST}/{SETTINGS.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

with engine.connect() as con:
    statement = text("CREATE EXTENSION IF NOT EXISTS unaccent;COMMIT;")
    con.execute(statement)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    """
    Get a database session.

    Yields
    ------
    SessionLocal
        Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
