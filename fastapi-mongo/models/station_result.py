from beanie import Document, PydanticObjectId
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class UserAnswer(BaseModel):
    question_id: PydanticObjectId
    answer_content: str
    evaluation: str

class StationResult(Document):
    session_id: PydanticObjectId
    station_id: PydanticObjectId
    exam_result_id: PydanticObjectId
    type: str
    user_answer: List[UserAnswer]
    score: int
    evaluation: str

    class Settings:
        name = "station_results"
        indexes = [
            [
                ("session_id", 1),
                ("station_id", 1)
            ]
        ]
        
    