from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

from models.StationModel import Station
from config.database import db

class StationRepository:
    def __init__(self):
        self.collection: AsyncIOMotorCollection = db["Station"]

    async def create(self, station: Station) -> Station:
        data = station.model_dump(by_alias=True, exclude={"stationId"})
        result = await self.collection.insert_one(data)
        station.stationId = result.inserted_id
        return station

    async def getAll(self) -> List[Station]:
        stations = []
        async for document in self.collection.find():
            stations.append(Station(**document))
        return stations

    async def getById(self, stationId: str) -> Optional[Station]:
        document = await self.collection.find_one({"_id": ObjectId(stationId)})
        if document:
            return Station(**document)
        return None

    async def getByPatientId(self, patientId: str) -> List[Station]:
        stations = []
        
        if not ObjectId.is_valid(patientId):
            return []
        
        async for document in self.collection.find({"patientId": ObjectId(patientId)}):
            stations.append(Station(**document))
        return stations

    async def getByType(self, stationType: str) -> List[Station]:
        stations = []
        async for document in self.collection.find({"type": stationType}):
            stations.append(Station(**document))
        return stations

    async def update(self, stationId: str, updateData: dict) -> bool:
        if not updateData:
            return False
        if not ObjectId.is_valid(stationId):
            return False
        
        result = await self.collection.update_one(
            {"_id": ObjectId(stationId)},
            {"$set": updateData}
        )
        return result.modified_count > 0

    async def delete(self, stationId: str) -> bool:
        if not ObjectId.is_valid(stationId):
            return False
        
        result = await self.collection.delete_one({"_id": ObjectId(stationId)})
        return result.deleted_count > 0
    
