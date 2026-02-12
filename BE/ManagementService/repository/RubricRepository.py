from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

from models.RubricModel import Rubric
from config.database import db

class RubricRepository:
    def __init__(self):
        self.collection: AsyncIOMotorCollection = db["Rubric"]

    async def create(self, rubric: Rubric) -> Rubric:
        data = rubric.model_dump(by_alias=True, exclude={"rubricId"})
        result = await self.collection.insert_one(data)
        rubric.rubricId = result.inserted_id
        return rubric
        
    async def getAll(self) -> List[Rubric]:
            rubrics: List[Rubric] = []
            async for document in self.collection.find():
                rubrics.append(Rubric(**document))
            return rubrics
        
    async def getById(self, rubricId: str) -> Optional[Rubric]:
        document = await self.collection.find_one({"_id": ObjectId(rubricId)})
        if document:
            return Rubric(**document)
        return None
        
    async def getByIds(self, rubricIds: List[str]) -> List[Rubric]:
        objectIds = [ObjectId(rid) for rid in rubricIds]
        rubrics: List[Rubric] = []
        async for document in self.collection.find(
            {"_id": {"$in": objectIds}}
        ):
            rubrics.append(Rubric(**document))
        return rubrics
    
    async def update(self, rubricId: ObjectId, updateData: dict) -> bool:
        if not updateData:
            return False
        
        if "_id" in updateData:
            del updateData["_id"]
        
        result = await self.collection.update_one(
            {"_id": rubricId},
            {"$set": updateData}
        )
        return result.modified_count > 0
    
    async def delete(self, rubricId: ObjectId) -> bool:
        result = await self.collection.delete_one({"_id": rubricId})
        return result.deleted_count > 0