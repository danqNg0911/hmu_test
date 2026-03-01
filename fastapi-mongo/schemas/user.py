from pydantic import BaseModel, EmailStr
from fastapi.security import HTTPBasicCredentials
from typing import Optional
from beanie import PydanticObjectId

class UserSignIn(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {"username": "OSCE_001", "password": "123456"}
        }

class UserCreate(BaseModel):
    name: str
    username: str
    password: str
    email: EmailStr
    role: str = "user"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Nguyen Van A",
                "username": "OSCE_001",
                "password": "123456",
                "email": "HMU@gmail.com",
                "role": "user"
            }
        }

class UserData(BaseModel):
    id: PydanticObjectId
    name: str
    username: str
    email: EmailStr
    role: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "69a2f1b5f3c42f3227ac9405",
                "name": "Nguyen Van A",
                "username": "OSCE_001",
                "email": "HMU@gmail.com",
                "role": "user"
            }
        }