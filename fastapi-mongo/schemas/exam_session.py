from pydantic import BaseModel
from typing import List, Optional
from beanie import PydanticObjectId

class ExamSessionCreate(BaseModel):
    user_id: str
    stations: Optional[List[PydanticObjectId]] = None
    expected_time: Optional[str] = None
    status: str = "IN_PROGRESS"
    current_station: Optional[int] = 1

class ExamSessionUpdate(BaseModel):
    status: Optional[str] = None
    current_station: Optional[int] = None

class ExamSessionResponse(ExamSessionCreate):
    id: PydanticObjectId