from BE.ExamService.database import db
from BE.ExamService.Models.StationModel import Station

class StationRepository:
    collection = db["stations"]
    
    async def create(self, station: Station):
        result = await self.collection.insert_one(station.dict(exclude={"_id"}))
        return str(result.inserted_id)
    
    async def find_by_id(self, id: str):
        return await self.collection.find_one({"_id": id})
    