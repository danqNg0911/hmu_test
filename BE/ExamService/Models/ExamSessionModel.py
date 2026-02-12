from BE.ExamService.Models import PyObjectId
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ExamSession(BaseModel):
    _id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId
    scenario_id: PyObjectId
    status: str
    current_station: str
    expected_time: datetime