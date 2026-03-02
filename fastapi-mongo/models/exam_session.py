from beanie import Document, PydanticObjectId
from typing import List, Optional
from datetime import datetime

class ExamSession(Document):
    user_id: PydanticObjectId
    stations: Optional[List[PydanticObjectId]] = None
    status: str
    current_station: Optional[int] = None
    expected_time: Optional[datetime] = None

    class Settings:
        name = "Exam_sessions"
        