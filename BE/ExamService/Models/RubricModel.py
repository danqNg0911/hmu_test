from BE.ExamService.Models import PyObjectId
from pydantic import BaseModel, Field
from typing import Optional

class Rubric(BaseModel):
    _id: Optional[PyObjectId] = Field(alias="_id")
    description: str
    max_score: int