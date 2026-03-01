from beanie import Document, PydanticObjectId
from typing import List
from datetime import datetime

class ExamSession(Document):
    user_id: PydanticObjectId
    stations: List[PydanticObjectId]
    status: str
    current_station: int
    expected_time: datetime

    class Settings:
        name = "Exam_sessions"
        