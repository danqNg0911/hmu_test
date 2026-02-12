from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from commons.PyObjectId import PyObjectId
from commons.enums import FindingTypeEnum, StationTypeEnum

class PresentedFinding(BaseModel):
    type: FindingTypeEnum
    title: Optional[str] = None
    content: Optional[str] = None

class Station(BaseModel):
    stationId: Optional[PyObjectId] = Field(alias="_id", default=None)
    patientId: PyObjectId
    type: StationTypeEnum
    presentedFindings: List[PresentedFinding] = []
    questions: List[PyObjectId] = []
    time: int

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )