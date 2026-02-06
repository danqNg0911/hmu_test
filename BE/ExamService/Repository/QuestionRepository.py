from BE.ExamService.database import db
from BE.ExamService.Models.QuestionModel import Question

class QuestionRepository:
    collection = db["questions"]
    
    async def create(self, question: Question):
        result = await self.collection.insert_one(question.dict(exclude={"_id"}))
        return str(result.inserted_id)
    
    async def find_by_id(self, id: str):
        return await self.collection.find_one({"_id": id})
    