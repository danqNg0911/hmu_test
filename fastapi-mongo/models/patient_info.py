from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from typing import List

class PatientInfo(Document):
    version: str
    name: str
    age: int
    gender: str
    avt_url: str
    voice_id: str
    description: str
    stationIds: List[PydanticObjectId]  # Kiểu dữ liệu chuẩn của Beanie cho ObjectId

    class Settings:
        name = "patient_info"

