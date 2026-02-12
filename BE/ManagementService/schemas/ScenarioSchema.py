from pydantic import BaseModel, ConfigDict
from typing import List
from commons.PyObjectId import PyObjectId
from schemas.PatientInfoSchema import PatientResponse
from schemas.StationSchema import StationResponse

class ScenarioStationDetail(BaseModel):
    patient: PatientResponse
    station: StationResponse

class Scenario(BaseModel):
    scenarioId: PyObjectId
    examStations: List[ScenarioStationDetail] = []

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )