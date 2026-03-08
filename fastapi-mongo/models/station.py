from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from typing import List, Optional

class Rubric(BaseModel):
    description: str
    max_score: int

class Question(BaseModel):
    question_content: str
    expected_ans: Optional[str] = None
    rubrics: List[Rubric]

class PresentedFinding(BaseModel):
    section_id: str
    type: str
    title: str
    content: str

class Station(Document):
    patient_info_id: Optional[PydanticObjectId] = None
    name: str
    type: str
    presented_findings: Optional[List[PresentedFinding]] = None
    questions: List[Question]
    time: int

    class Settings:
        name = "Stations"
