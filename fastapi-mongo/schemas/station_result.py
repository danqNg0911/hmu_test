from beanie import Document, PydanticObjectId
from typing import List, Optional
from pydantic import BaseModel

class UserAnswerSchema(BaseModel):
    question_id: PydanticObjectId
    answer_content: str
    evaluation: str

class StationResultCreate(BaseModel):
    station_id: PydanticObjectId
    patient_id: PydanticObjectId
    exam_result_id: PydanticObjectId
    type: str
    user_answer: Optional[List[UserAnswerSchema]] = None
    score: Optional[int]
    evaluation: Optional[str]

class StationResultResponse(StationResultCreate):
    id: PydanticObjectId

