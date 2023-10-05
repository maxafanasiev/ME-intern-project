from typing import Optional

from app.repository.quizzes import QuizRepository
from app.db.models import User as UserModel, Quiz


class QuizService:
    def __init__(self, quiz_repo: QuizRepository):
        self.quiz_repo: QuizRepository = quiz_repo()

    async def create_quiz(self, quiz, company_id: int, current_user: UserModel) -> Quiz:
        return await self.quiz_repo.add_one(quiz, company_id, current_user)

    async def get_quiz_by_id(self, quiz_id: int) -> Optional[Quiz]:
        return await self.quiz_repo.get_one(quiz_id)

    async def get_all_quizzes_in_company(self, company_id: int, page: int, size: int):
        return await self.quiz_repo.get_all_quizzes_in_company(company_id, page, size)

    async def update_quiz(self, quiz_id: int, data,
                          current_user: UserModel) -> Optional[Quiz]:
        return await self.quiz_repo.update_one(quiz_id, data, current_user)

    async def delete_quiz(self, quiz_id: int, current_user: UserModel) -> Optional[Quiz]:
        return await self.quiz_repo.delete_one(quiz_id, current_user)
