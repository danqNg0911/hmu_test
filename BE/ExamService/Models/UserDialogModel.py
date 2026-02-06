from BE.ExamService.Models.PyObjectId import PyObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

class UserDialog(BaseModel):
    _id: Optional[PyObjectId] = Field(alias="_id")
    messages: List[PyObjectId]
    evaluation: List[dict]