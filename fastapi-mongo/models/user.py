from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr


class User(Document):
    name: str
    username: str
    password: str
    email: EmailStr
    role: str

    class Settings:
        name = "Users"

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


class UserSignIn(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {"username": "OSCE_001", "password": "123456"}
        }


class UserData(BaseModel):
    name: str
    email: EmailStr


    class Config:
        json_schema_extra = {
            "example": {
                "name": "Nguyen Van A",
                "email": "HMU@gmail.com"
            }
        }

