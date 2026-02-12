from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

from models.PatientInfoModel import PatientInfo
from config.database import db

class PatientRepository:
    def __init__(self):
        self.collection: AsyncIOMotorCollection = db["PatientInfo"]

    async def create(self, patient: PatientInfo) -> PatientInfo:
        data = patient.model_dump(by_alias=True, exclude={"patientId"})
        result = await self.collection.insert_one(data)
        patient.patientId = result.inserted_id
        return patient

    async def getAll(self) -> List[PatientInfo]:
        patients = []
        async for document in self.collection.find():
            patients.append(PatientInfo(**document))
        return patients
    
    async def getById(self, patientid: str) -> Optional[PatientInfo]:
        document = await self.collection.find_one(
            {"_id": ObjectId(patientid)}
        )
        if document:
            return PatientInfo(**document)
        return None
    
    async def update(self, patientId: str, updateData: dict) -> bool:
        if not updateData:
            return False
        
        result = await self.collection.update_one(
            {"_id": ObjectId(patientId)},
            {"$set": updateData}
        )
        return result.modified_count > 0

    async def delete(self, patientId: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(patientId)})
        return result.deleted_count > 0