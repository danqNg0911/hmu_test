from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import List

class Rubric(BaseModel):
    description: str
    max_score: int

class Question(BaseModel):
    question_content: str
    expected_ans: str
    rubric: List[Rubric]

class PresentedFinding(BaseModel):
    section_id: str
    type: str
    title: str
    content: str

class Station(Document):
    type: str
    presented_findings: List[PresentedFinding]
    questions: List[Question]
    time: int

    class Settings:
        name = "Stations"
