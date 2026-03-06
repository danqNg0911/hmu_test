from beanie import Document, PydanticObjectId
from datetime import datetime
from typing import Optional


class ExamStation(Document):
    session_id: PydanticObjectId
    user_id: PydanticObjectId
    station_id: PydanticObjectId

    station_number: int

    status: str  # có thể bao gồm 4 trạng thái: NOT_STARTED, IN_PROGRESS, SUBMITTED, TIMEOUT

    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    time_limit: Optional[int] = None  

    class Settings:
        name = "Exam_stations"