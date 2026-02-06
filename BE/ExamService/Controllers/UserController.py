from BE.ExamService.Repository.UserRepository import UserRepository
from BE.ExamService.Models.UserModel import User

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    async def create_user(self, user: User):
        existing = await self.repo.find_by_email(user.email)
        if existing:
            raise ValueError("Email already exists")
        return await self.repo.create(user)