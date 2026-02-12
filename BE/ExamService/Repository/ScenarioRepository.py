from BE.ExamService.database import db
from BE.ExamService.Models.ScenarioModel import Scenario

class ScenarioRepository:
    collection = db["scenarios"]
    
    async def create(self, scenario: Scenario):
        result = await self.collection.insert_one(scenario.dict(exclude={"_id"}))
        return str(result.inserted_id)
    
    async def find_by_id(self, id: str):
        return await self.collection.find_one({"_id": id})
    