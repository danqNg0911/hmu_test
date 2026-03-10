from beanie import Document, PydanticObjectId
from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel

class ExamResultCreate(BaseModel):
    user_id: PydanticObjectId 
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    total_score: Optional[int] = None
    overall_feedback: Optional[str] = None

class ExamResultResponse(ExamResultCreate):
    id: PydanticObjectId

class ExamResultUpdate(BaseModel):
    end_at: datetime
    total_score: int
    overall_feedback: str

class StationSummaryResponse(BaseModel):
    station_id: PydanticObjectId
    station_name: str
    score: Optional[float] = 0
    evaluation: Any

class ExamResultResponse(BaseModel):
    session_id: PydanticObjectId
    user_id: PydanticObjectId 
    start_at: datetime
    end_at: datetime
    total_score: int
    overall_feedback: Optional[str] = None
    stations_summary: Optional[list[StationSummaryResponse]] = None

    class Settings:
        name = "Exam_results"
    