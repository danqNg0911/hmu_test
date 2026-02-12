from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.database import connect_to_database, close_database_connection

from controllers.PatientInfoController import router as PatientInfoRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_database()
    yield
    await close_database_connection()

app = FastAPI(lifespan=lifespan)

app.include_router(
    PatientInfoRouter,
    prefix="/api/v1/patients",
    tags=["PatientInfo"]
)

