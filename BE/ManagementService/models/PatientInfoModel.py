from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from commons.enums import GenderEnum
from commons.PyObjectId import PyObjectId

class PatientInfo(BaseModel):
    patientId: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    age: int
    gender: GenderEnum
    avtUrl: Optional[str] = None
    voiceId: Optional[str] = None
    description: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )