from beanie import Document, PydanticObjectId
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ExamResultCreate(BaseModel):
    user_id: PydanticObjectId 
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    total_score: Optional[int] = None
    overall_feedback: Optional[str] = None

class ExamResultResponse(ExamResultCreate):
    id: PydanticObjectId

class ExamResultUpdate(BaseModel):
    end_at: datetime
    total_score: int
    overall_feedback: str
        
    