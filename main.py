from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.config.settings import Settings
from src.routers import counseling_session
from src.config.db_config import engine, Base
from fastapi.middleware.cors import CORSMiddleware

settings = Settings()
app = FastAPI(title=settings.PROJECT_NAME)

Base.metadata.create_all(bind=engine)

app.include_router(counseling_session.router)

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