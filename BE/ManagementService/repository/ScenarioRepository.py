
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import List, Optional
from bson import ObjectId
from config.database import db

from models.ScenarioModel import Scenario

class ScenarioRepository:
    def __init__(self):
        self.collection: AsyncIOMotorCollection = db["Scenario"]

    async def create(self, scenario: Scenario) -> Scenario:
        data = scenario.model_dump(by_alias=True, exclude={"scenarioId"})
        result = await self.collection.insert_one(data)
        scenario.scenarioId = result.inserted_id
        return scenario

    async def getAll(self) -> List[Scenario]:
        scenarios = []
        async for document in self.collection.find():
            scenarios.append(Scenario(**document))
        return scenarios


    async def getById(self, scenario_id) -> Optional[Scenario]:
        document = await self.collection.find_one({"_id": ObjectId(scenario_id)})
        if document:
            return Scenario(**document)
        return None

    async def update(self, scenarioId: str, updateData: dict) -> bool:
        if not updateData:
            return False
        
        if "_id" in updateData:
            del updateData["_id"]
        
        result = await self.collection.update_one(
            {"_id": ObjectId(scenarioId)},
            {"$set": updateData}
        )
        return result.modified_count > 0
    
    async def delete(self, scenarioId: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(scenarioId)})
        return result.deleted_count > 0
    
    async def addStationToScenario(self,  scenarioId: str, stationId: str) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(scenarioId)},
            {"$addToSet": {"stationIds": ObjectId(stationId)}}
        )
        return result.modified_count > 0

    async def removeStationFromScenario(self, scenarioId: str, stationId: str) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(scenarioId)},
            {"$pull": {"stationIds": ObjectId(stationId)}}
        )
        return result.modified_count > 0
        

    