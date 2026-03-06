from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import models as models


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")
    
    DATABASE_URL: Optional[str] = None

    # JWT
    secret_key: str = "secret"
    algorithm: str = "HS256"
    
    minio_endpoint: Optional[str] = None
    minio_root_user: Optional[str] = None
    minio_root_password: Optional[str] = None


async def initiate_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(
       #database=client.get_default_database(), document_models=models.__all__
       database=client["HMU-Test"], document_models=models.__all__
    )
