from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from commons.PyObjectId import PyObjectId

class Rubric(BaseModel):
    rubricId: Optional[PyObjectId] = Field(alias="_id", default=None)
    description: str
    maxScore: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )