from BE.ExamService.database import db
from BE.ExamService.Models.PatientInfoModel import PatientInfo

class PatientInfoRepository:
    collection = db["patient_infos"]
    
    async def create(self, patient_info: PatientInfo):
        result = await self.collection.insert_one(patient_info.dict(exclude={"_id"}))
        return str(result.inserted_id)
    
    async def find_by_id(self, id: str):
        return await self.collection.find_one({"_id": id})
    