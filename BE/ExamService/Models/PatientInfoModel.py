from BE.ExamService.Models.PyObjectId import PyObjectId
from pydantic import BaseModel, Field
from typing import Optional

class PatientInfo(BaseModel):
    _id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    age: int
    gender: str
    avt_url: Optional[str] = None
    voice_id: Optional[str] = None
    description: str