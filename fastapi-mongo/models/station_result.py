from beanie import Document, PydanticObjectId
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class UserAnswer(BaseModel):
    question_id: PydanticObjectId
    answer_content: str
    evaluation: Optional[str] = None

class StationResult(Document):
    session_id: PydanticObjectId
    station_id: PydanticObjectId
    type: str
    user_answer: Optional[List[UserAnswer]] = None
    score: Optional[int] = None
    evaluation: Optional[str] = None

    class Settings:
        name = "Station_results"