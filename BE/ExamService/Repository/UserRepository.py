from BE.ExamService.database import db
from BE.ExamService.Models.UserModel import User

class UserRepository:
    collection = db["users"]
    
    async def create(self, user: User):
        result = await self.collection.insert_one(user.dict(exclude={"_id"}))
        return str(result.inserted_id)
    
    async def find_by_id(self, id: str):
        return await self.collection.find_one({"_id": id})
    