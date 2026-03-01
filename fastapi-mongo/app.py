from fastapi import FastAPI, Depends
from routes.user import router as UserRouter
from routes.station import router as StationRouter
from routes.patient_info import router as PatientInfoRouter
from routes.exam_session import router as ExamSessionRouter
from routes.message import router as MessageRouter
from routes.exam_result import router as ExamResultRouter

from auth.jwt_bearer import JWTBearer
from config.config import initiate_database

app = FastAPI()

token_listener = JWTBearer()


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "HMU test"}


app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(StationRouter, tags=["Station"], prefix="/station")
app.include_router(PatientInfoRouter, tags=["Patient Info"], prefix="/patient-info")
app.include_router(ExamSessionRouter, tags=["Exam Session"], prefix="/session")
app.include_router(MessageRouter, tags=["Message"], prefix="/message")
app.include_router(ExamResultRouter, tags=["Exam Result"], prefix="/exam-result")
