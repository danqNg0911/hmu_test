from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from commons.PyObjectId import PyObjectId
from commons.enums import StationTypeEnum, FindingTypeEnum
from schemas.QuestionSchema import QuestionResponse
from schemas.PatientInfoSchema import PatientResponse

class PresentedFinding(BaseModel):
    type: FindingTypeEnum
    title: Optional[str] = None
    content: Optional[str] = None

class StationCreate(BaseModel):
    type: StationTypeEnum
    presentedFindings: List[PresentedFinding] = []
    questions: List[PyObjectId] = []
    time: int

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class StationResponse(BaseModel):
    stationId: PyObjectId = Field(alias="_id", default=None)
    patientInfo: Optional[PatientResponse] = None
    type: StationTypeEnum
    presentedFindings: List[PresentedFinding] = []
    questions: List[QuestionResponse] = []
    time: int

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class StationUpdate(BaseModel):
    type: Optional[StationTypeEnum] = None
    presentedFindings: Optional[List[PresentedFinding]] = None
    questions: Optional[List[PyObjectId]] = None
    time: Optional[int] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
