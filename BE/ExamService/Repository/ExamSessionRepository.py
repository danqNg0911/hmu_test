from BE.ExamService.database import db
from BE.ExamService.Models.ExamSessionModel import ExamSession

class ExamSessionRepository:
    collection = db["exam_sessions"]
    
    async def create(self, exam_session: ExamSession):
        result = await self.collection.insert_one(exam_session.dict(exclude={"_id"}))
        return str(result.inserted_id)
    
    async def find_by_id(self, id: str):
        return await self.collection.find_one({"_id": id})
    