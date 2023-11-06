from typing import Optional

from app.repository.questions import QuestionRepository
from app.db.models import User as UserModel, Question
from app.schemas.question_schemas import QuestionsListResponse


class QuestionService:
    def __init__(self, question_repo: QuestionRepository):
        self.question_repo: QuestionRepository = question_repo()

    async def create_question(self, quiz, quiz_id: int, current_user: UserModel) -> Question:
        return await self.question_repo.add_one(quiz, quiz_id, current_user)

    async def get_question_by_id(self, question_id: int) -> Optional[Question]:
        return await self.question_repo.get_one(question_id)

    async def get_all_question_in_quiz(self, quiz_id: int) -> QuestionsListResponse:
        return await self.question_repo.get_all_questions_in_quiz(quiz_id)

    async def update_question(self, quiz_id: int, data,
                              current_user: UserModel) -> Optional[Question]:
        return await self.question_repo.update_one(quiz_id, data, current_user)

    async def delete_question(self, quiz_id: int, current_user: UserModel) -> Optional[Question]:
        return await self.question_repo.delete_one(quiz_id, current_user)
