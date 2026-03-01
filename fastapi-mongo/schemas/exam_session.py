from pydantic import BaseModel
from typing import List, Optional
from beanie import PydanticObjectId

class ExamSessionCreate(BaseModel):
    user_id: str
    stations: List[PydanticObjectId]
    expected_time: str
    status: str = "IN_PROGRESS"
    current_station: int = 1

class ExamSessionUpdate(BaseModel):
    status: Optional[str] = None
    current_station: Optional[int] = None

class ExamSessionResponse(ExamSessionCreate):
    id: PydanticObjectId