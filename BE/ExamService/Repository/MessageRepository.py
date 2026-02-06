from BE.ExamService.database import db
from BE.ExamService.Models.MessageModel import Message

class MessageRepository:
    collection = db["messages"]
    
    async def create(self, message: Message):
        result = await self.collection.insert_one(message.dict(exclude={"_id"}))
        return str(result.inserted_id)
    
    async def find_by_id(self, id: str):
        return await self.collection.find_one({"_id": id})
    