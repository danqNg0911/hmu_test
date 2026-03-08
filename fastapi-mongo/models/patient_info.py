from beanie import Document
from typing import List, Optional

class PatientInfo(Document):
    version: str
    name: str
    age: int
    gender: str
    avt_url: str
    voice_id: str
    description: str

    class Settings:
        name = "Patient_infos"

