from pydantic import BaseModel
from typing import List, Optional
from beanie import PydanticObjectId

class PatientInfoCreate(BaseModel):
    version: str
    name: str
    age: int
    gender: str
    avt_url: str
    voice_id: str
    description: str

class PatientInfoUpdate(BaseModel):
    id: Optional[PydanticObjectId] = None
    version: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    avt_url: Optional[str] = None
    voice_id: Optional[str] = None
    description: Optional[str] = None

class PatientInfoResponse(PatientInfoCreate):
    id: PydanticObjectId

class StationBrief(BaseModel):
    station_id: str
    station_name: str

class PatientInfoDetailResponse(BaseModel):
    id: Optional[PydanticObjectId] = None
    version: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    avt_url: Optional[str] = None
    voice_id: Optional[str] = None
    description: Optional[str] = None
    stations_list: Optional[list[StationBrief]] = None