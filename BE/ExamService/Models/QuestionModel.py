from BE.ExamService.Models.PyObjectId import PyObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

class Question(BaseModel):
    _id: Optional[PyObjectId] = Field(alias="_id")
    question_content: str
    expected_answer: str
    rubrics: List[PyObjectId]