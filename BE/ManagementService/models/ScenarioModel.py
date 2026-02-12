from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from commons.PyObjectId import PyObjectId

class PreparedStation(BaseModel):
    stationId: Optional[PyObjectId] = None
    questionIds: list[PyObjectId] = []

class Scenario(BaseModel):
    scenarioId: PyObjectId = Field(alias="_id", default=None)
    examStations: list[PreparedStation] = []

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )