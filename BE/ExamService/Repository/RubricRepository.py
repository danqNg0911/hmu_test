from BE.ExamService.database import db
from BE.ExamService.Models.RubricModel import Rubric

class RubricRepository:
    collection = db["rubrics"]
    
    async def create(self, rubric: Rubric):
        result = await self.collection.insert_one(rubric.dict(exclude={"_id"}))
        return str(result.inserted_id)
    
    async def find_by_id(self, id: str):
        return await self.collection.find_one({"_id": id})
    