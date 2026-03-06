from beanie import Document, PydanticObjectId
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class ExamResult(Document):
    user_id: PydanticObjectId 
    start_at: datetime
    end_at: datetime
    total_score: int
    overall_feedback: Optional[str] = None

    class Settings:
        name = "Exam_results"
        
    