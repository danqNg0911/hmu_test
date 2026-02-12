from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from commons.enums import GenderEnum
from commons.PyObjectId import PyObjectId

class PatientCreate(BaseModel):
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

class PatientResponse(PatientCreate):
    patientId: Optional[PyObjectId] = Field(alias="_id", default=None)

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[GenderEnum] = None
    avtUrl: Optional[str] = None
    voiceId: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )