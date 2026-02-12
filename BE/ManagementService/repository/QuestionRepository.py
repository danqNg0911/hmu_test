from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

from models.QuestionModel import Question
from config.database import db

class QuestionRepository:
    def __init__(self):
        self.collection: AsyncIOMotorCollection = db["Question"]

    async def create(self, question: Question) -> Question:
        data = question.model_dump(by_alias=True, exclude={"questionId"})
        result = await self.collection.insert_one(data)
        question.questionId = result.inserted_id
        return question
    
    async def getAll(self) -> List[Question]:
        questions = []
        async for document in self.collection.find():
            questions.append(Question(**document))
        return questions

    async def getById(self, questionId: str) -> Optional[Question]:
        document = await self.collection.find_one({"_id": ObjectId(questionId)})
        if document:
            return Question(**document)
        return None

    async def getByIds(self, questionIds: List[str]) -> List[Question]:
        objectIds = [ObjectId(qid) for qid in questionIds if ObjectId.is_valid(qid)]
        if not objectIds:
            return []
        
        questions: List[Question] = []

        async for document in self.collection.find({"_id": {"$in": objectIds}}):
            questions.append(Question(**document))
            
        return questions
 
    async def update(self, questionId: str, updateData: dict) -> bool:
        if not updateData:
            return False
        
        result = await self.collection.update_one(
            {"_id": ObjectId(questionId)},
            {"$set": updateData}
        )
        return result.modified_count > 0

    async def delete(self, questionId: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(questionId)})
        return result.deleted_count > 0