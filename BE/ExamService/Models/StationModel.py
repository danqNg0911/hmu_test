from BE.ExamService.Models import PyObjectId
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Station(BaseModel):
    _id: Optional[PyObjectId] = Field(alias="_id")
    patient_id: PyObjectId
    type: str
    presented_findings: List[dict]
    questions: List[PyObjectId]
    time : int