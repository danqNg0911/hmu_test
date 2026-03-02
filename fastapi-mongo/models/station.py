from beanie import Document
from pydantic import BaseModel, EmailStr
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
    type: str
    presented_findings: Optional[List[PresentedFinding]] = None
    questions: List[Question]
    time: int

    class Settings:
        name = "Stations"
