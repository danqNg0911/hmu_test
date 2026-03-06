from fastapi import APIRouter, Body, Depends, status
from beanie import PydanticObjectId
from pydantic import BaseModel
from typing import List, Optional

from models.exam_session import ExamSession
from schemas.exam_session import ExamSessionCreate, ExamSessionResponse, ExamSessionUpdate
from service.ExamService.ExamSessionService import ExamSessionService
from schemas.station_result import UserAnswerRequest

router = APIRouter()

class StartExamRequest(BaseModel):
    user_id: str
    total_station: int

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Start a new exam session"
)
async def start_exam_session(
    payload: StartExamRequest,
    service: ExamSessionService = Depends(ExamSessionService)
):
    return await service.startExamSession(payload.user_id, payload.total_station)


@router.get(
    "/{session_id}/station",
    status_code=status.HTTP_200_OK,
    summary="Get current station of the session"
)
async def get_current_station(
    session_id: PydanticObjectId,
    service: ExamSessionService = Depends(ExamSessionService)
):
    return await service.getCurrentStation(session_id)


@router.post(
    "/{session_id}/station/submission",
    status_code=status.HTTP_200_OK,
    summary="Submit current station and get next station data"
)
async def submit_station(
    session_id: PydanticObjectId,
    station_type: str,
    answers: Optional[List[UserAnswerRequest]] = None,
    service: ExamSessionService = Depends(ExamSessionService)
):
    return await service.submitCurrentStation(session_id, station_type, answers)