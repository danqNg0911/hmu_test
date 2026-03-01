from beanie import Document, PydanticObjectId
from typing import List
from datetime import datetime
from pydantic import BaseModel

class UserDialogSchema(BaseModel):
    message: PydanticObjectId
    evaluation: str

class UserAnswerSchema(BaseModel):
    question_id: PydanticObjectId
    answer_content: str
    evaluation: str

class StationResultSchema(BaseModel):
    station_id: PydanticObjectId
    patient_id: PydanticObjectId
    type: str
    user_dialogs: List[UserDialogSchema]
    user_answer: List[UserAnswerSchema]
    score: int
    evaluation: str

class ExamResultCreate(BaseModel):
    user_id: PydanticObjectId 
    start_at: datetime
    end_at: datetime
    station_results: List[StationResultSchema]
    overall_feedback: str

class ExamResultResponse(ExamResultCreate):
    id: PydanticObjectId
        
    