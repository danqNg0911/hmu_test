from beanie import Document, PydanticObjectId
from typing import List, Optional, Dict, Any
from datetime import datetime

class ExamSession(Document):
    user_id: PydanticObjectId
    stations: Optional[List[PydanticObjectId]] = None
    status: str
    current_station: Optional[int] = None
    patients_snapshot: Dict[str, Any] = {}

    #expected_time: Optional[datetime] = None

    class Settings:
        name = "Exam_sessions"
        