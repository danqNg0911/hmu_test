from BE.ExamService.database import db
from BE.ExamService.Models.UserAnswerModel import UserAnswer

class UserAnswerRepository:
    collection = db["user_answers"]
    
    async def create(self, user_answer: UserAnswer):
        result = await self.collection.insert_one(user_answer.dict(exclude={"_id"}))
        return str(result.inserted_id)
    
    async def find_by_id(self, id: str):
        return await self.collection.find_one({"_id": id})
    