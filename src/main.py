from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from fastapi.responses import RedirectResponse

from src.config.db_config import Base, engine
from src.config.settings import SETTINGS
from src.routers import doctor, image, patient, prediction
from src.services.doctor import get_current_doctor

app = FastAPI(title=SETTINGS.PROJECT_NAME)

Base.metadata.create_all(bind=engine)

app.include_router(
    doctor.router,
    prefix=f"/{SETTINGS.API_VERSION}",
)
app.include_router(
    patient.router,
    dependencies=[Depends(get_current_doctor)],
    prefix=f"/{SETTINGS.API_VERSION}",
)
app.include_router(
    image.router,
    dependencies=[Depends(get_current_doctor)],
    prefix=f"/{SETTINGS.API_VERSION}",
)
app.include_router(
    prediction.router,
    dependencies=[Depends(get_current_doctor)],
    prefix=f"/{SETTINGS.API_VERSION}",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
