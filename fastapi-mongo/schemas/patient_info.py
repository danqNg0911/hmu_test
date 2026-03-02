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
    stationIds: Optional[List[PydanticObjectId]] = None

class PatientInfoUpdate(BaseModel):
    version: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    avt_url: Optional[str] = None
    voice_id: Optional[str] = None
    description: Optional[str] = None
    stationIds: Optional[List[PydanticObjectId]] = None

class PatientInfoResponse(PatientInfoCreate):
    id: PydanticObjectId