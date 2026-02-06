from motor.motor_asyncio import AsyncIOMotorClient
from BE.ExamService.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DB_NAME]