from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from commons.PyObjectId import PyObjectId

class Question(BaseModel):
    questionId: Optional[PyObjectId] = Field(alias="_id", default=None)
    questionContent: str
    expectedAnswer: Optional[str] = None
    rubrics: List[PyObjectId] = []

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )