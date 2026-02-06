from BE.ExamService.database import db
from BE.ExamService.Models.UserDialogModel import UserDialog

class UserDialogRepository:
    collection = db["user_dialogs"]
    
    async def create(self, user_dialog: UserDialog):
        result = await self.collection.insert_one(user_dialog.dict(exclude={"_id"}))
        return str(result.inserted_id)
    
    async def find_by_id(self, id: str):
        return await self.collection.find_one({"_id": id})
    