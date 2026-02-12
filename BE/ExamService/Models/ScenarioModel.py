from BE.ExamService.Models import PyObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

class Scenario(BaseModel):
    _id: Optional[PyObjectId] = Field(alias="_id")
    station_requests: List[dict]