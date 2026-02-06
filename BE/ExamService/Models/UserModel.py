from BE.ExamService.Models import PyObjectId
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    _id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    username: str
    password: str
    email: str
    role: str