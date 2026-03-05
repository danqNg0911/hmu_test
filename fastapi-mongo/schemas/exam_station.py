from beanie import PydanticObjectId
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ExamStationCreate(BaseModel):
    session_id: PydanticObjectId
    user_id: PydanticObjectId
    station_id: PydanticObjectId
    station_number: int
    status: str
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    time_limit: Optional[int]  = None

class ExamStationResponse(ExamStationCreate):
    id: PydanticObjectId 

class ExamStationUpdate(BaseModel):
    station_number: int
    status: str
    remaining_time: datetime
