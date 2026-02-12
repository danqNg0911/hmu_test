from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from commons.PyObjectId import PyObjectId

class RubricCreate(BaseModel):
    description: str
    maxScore: float = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class RubricResponse(RubricCreate):
    rubricId: PyObjectId = Field(alias="_id", default=None)

class RubricUpdate(BaseModel):
    description: Optional[str] = None
    maxScore: Optional[float] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )


