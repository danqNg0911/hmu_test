from BE.ExamService.Models import PyObjectId
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Message(BaseModel):
    _id: Optional[PyObjectId] = Field(alias="_id")
    sender: PyObjectId
    recipient: PyObjectId
    messageType: str
    content: str
    timestamp: datetime