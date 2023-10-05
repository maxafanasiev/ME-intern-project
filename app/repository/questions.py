from datetime import datetime
from typing import Optional

from sqlalchemy import insert, select

from app.db.db_connect import get_db
from app.db.models import Quiz, User as UserModel, Question
from app.repository.quizzes import QuizRepository
from app.schemas.question_schemas import QuestionsListResponse
from app.services.action_services import actions
from app.utils.repository import SQLAlchemyRepository


class QuestionRepository(SQLAlchemyRepository):
    model = Question

    async def add_one(self, data, quiz_id: int, current_user: UserModel) -> Question:
        async for session in get_db():
            quiz = await QuizRepository().get_one(quiz_id)
            if (await actions.validate_user_is_owner(current_user.id, quiz.quiz_company_id, session)
                    or await actions.validate_user_is_admin(current_user.id, quiz.quiz_company_id, session)):
                data_dict = dict(data)
                query = insert(self.model).values(**data_dict).returning(self.model)
                res = await session.execute(query)
                db_question = res.scalar_one()
                db_question.question_quiz_id = quiz_id
                await session.commit()
                return db_question

    async def update_one(self, question_id: int, data, current_user: UserModel) -> Optional[Question]:
        async for session in get_db():
            question = await self.get_one(question_id)
            quiz = await QuizRepository().get_one(question.question_quiz_id)
            if (await actions.validate_user_is_owner(current_user.id, quiz.quiz_company_id, session)
                    or await actions.validate_user_is_admin(current_user.id, quiz.quiz_company_id, session)):

                for field, value in data.model_dump().items():
                    if value is not None:
                        setattr(question, field, value)
                question.updated_at = datetime.now()
                await session.commit()
                return question

    async def delete_one(self, question_id: int, current_user: UserModel) -> Optional[Question]:
        async for session in get_db():
            question = await self.get_one(question_id)
            quiz = await QuizRepository().get_one(question.question_quiz_id)
            if (await actions.validate_user_is_owner(current_user.id, quiz.quiz_company_id, session)
                    or await actions.validate_user_is_admin(current_user.id, quiz.quiz_company_id, session)):
                await session.delete(question)
                await session.commit()
                return question

    async def get_all_questions_in_quiz(self, quiz_id: int) -> QuestionsListResponse:
        async for session in get_db():
            query = select(self.model).where(self.model.question_quiz_id == quiz_id)
            res = await session.execute(query)
            table_name = self.model.__tablename__
            return {table_name: res.scalars().all()}
