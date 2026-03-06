from beanie import Document, PydanticObjectId
from typing import List, Optional
from pydantic import BaseModel

class UserAnswerRequest(BaseModel):
    question_id: PydanticObjectId
    answer_content: str

class UserAnswer(UserAnswerRequest):
    evaluation: Optional[str] = None

class StationResultCreate(BaseModel):
    session_id: PydanticObjectId
    station_id: PydanticObjectId
    type: str
    user_answer: Optional[List[UserAnswer]] = None
    score: Optional[int]
    evaluation: Optional[str]

class StationResultResponse(StationResultCreate):
    id: PydanticObjectId

