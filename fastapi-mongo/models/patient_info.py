from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from typing import List, Optional

class PatientInfo(Document):
    version: str
    name: str
    age: int
    gender: str
    avt_url: str
    voice_id: str
    description: str
    stationIds: Optional[List[PydanticObjectId]] = None

    class Settings:
        name = "Patient_infos"

