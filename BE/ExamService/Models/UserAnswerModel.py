from BE.ExamService.Models.PyObjectId import PyObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

class UserAnswer(BaseModel):
    _id: Optional[PyObjectId] = Field(alias="_id")
    question_id: PyObjectId
    answer_content: str
    evaluation: List[dict]