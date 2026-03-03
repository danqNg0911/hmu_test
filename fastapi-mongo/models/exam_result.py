from beanie import Document, PydanticObjectId
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class UserDialog(BaseModel):
    message: PydanticObjectId
    evaluation: str

class UserAnswer(BaseModel):
    question_id: PydanticObjectId
    answer_content: str
    evaluation: str

class StationResult(BaseModel):
    station_id: PydanticObjectId
    patient_id: PydanticObjectId
    type: str
    user_dialogs: List[UserDialog]
    user_answer: List[UserAnswer]
    score: int
    evaluation: str

class ExamResult(Document):
    user_id: PydanticObjectId 
    start_at: datetime
    end_at: datetime
    station_results: Optional[List[StationResult]] = None
    overall_feedback: str

    class Settings:
        name = "Exam_results"
        
    