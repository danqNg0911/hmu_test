from pydantic import BaseModel
from typing import List, Optional, Any
from beanie import PydanticObjectId

class ExamSessionCreate(BaseModel):
    user_id: PydanticObjectId
    stations: Optional[List[PydanticObjectId]] = None
    expected_time: Optional[str] = None
    status: str = "IN_PROGRESS"
    current_station: Optional[int] = 1
    patients_snapshot: Optional[dict[str, Any]] = None

class ExamSessionUpdate(BaseModel):
    status: Optional[str] = None
    current_station: Optional[int] = None

class ExamSessionResponse(ExamSessionCreate):
    id: PydanticObjectId

class ExamSessionStartResponse(BaseModel):
    id: PydanticObjectId
    current_station: int

    