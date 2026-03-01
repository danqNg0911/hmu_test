from pydantic import BaseModel
from typing import List, Optional
from beanie import PydanticObjectId

class RubricSchema(BaseModel):
    description: str
    max_score: int

class QuestionSchema(BaseModel):
    question_content: str
    expected_ans: str
    rubric: List[RubricSchema]

class PresentedFindingSchema(BaseModel):
    section_id: str
    type: str
    title: str
    content: str

class StationCreate(BaseModel):
    type: str
    presented_findings: List[PresentedFindingSchema]
    questions: List[QuestionSchema]
    time: int

class StationUpdate(BaseModel):
    type: Optional[str] = None
    presented_findings: Optional[List[PresentedFindingSchema]] = None
    questions: Optional[List[QuestionSchema]] = None
    time: Optional[int] = None

class StationResponse(StationCreate):
    id: PydanticObjectId
