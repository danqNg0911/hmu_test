from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from commons.enums import RoleEnum
from commons.PyObjectId import PyObjectId

class User(BaseModel):
    userId: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    username: str
    password: str
    email: EmailStr
    role: RoleEnum

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )