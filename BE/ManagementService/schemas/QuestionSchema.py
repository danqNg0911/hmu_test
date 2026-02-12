from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from commons.PyObjectId import PyObjectId
from schemas.RubricSchema import RubricResponse 

class QuestionCreate(BaseModel):
    questionContent: str
    expectedAnswer: Optional[str] = None
    rubrics: List[PyObjectId] = []

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class QuestionResponse(BaseModel):
    questionId: PyObjectId = Field(alias="_id")
    questionContent: str
    expectedAnswer: Optional[str] = None
    rubrics: List[RubricResponse] = []

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class QuestionUpdate(BaseModel):
    questionContent: Optional[str] = None
    expectedAnswer: Optional[str] = None
    rubrics: Optional[List[PyObjectId]] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )