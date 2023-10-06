from datetime import datetime
from typing import Optional

from sqlalchemy import insert, select

from app.db.db_connect import get_db
from app.db.models import Quiz, User as UserModel, Result
from app.schemas.quiz_schemas import QuizListResponse
from app.services.action_services import actions
from app.services.exceptions import NotMemberException, NotValidQuizException
from app.services.result_services import results
from app.utils.repository import SQLAlchemyRepository


class QuizRepository(SQLAlchemyRepository):
    model = Quiz

    async def add_one(self, data, company_id: int, current_user: UserModel) -> Quiz:
        async for session in get_db():
            if (await actions.validate_user_is_owner(current_user.id, company_id, session)
                    or await actions.validate_user_is_admin(current_user.id, company_id, session)):
                data_dict = dict(data)
                query = insert(self.model).values(**data_dict).returning(self.model)
                res = await session.execute(query)
                db_quiz = res.scalar_one()
                db_quiz.quiz_company_id = company_id
                await session.commit()
                return db_quiz

    async def update_one(self, quiz_id: int, data, current_user: UserModel) -> Optional[Quiz]:
        async for session in get_db():
            quiz = await self.get_one(quiz_id)
            if (await actions.validate_user_is_owner(current_user.id, quiz.quiz_company_id, session)
                    or await actions.validate_user_is_admin(current_user.id, quiz.quiz_company_id, session)):

                for field, value in data.model_dump().items():
                    if value is not None:
                        setattr(quiz, field, value)
                quiz.updated_at = datetime.now()
                await session.commit()
                return quiz

    async def delete_one(self, quiz_id: int, current_user: UserModel) -> Optional[Quiz]:
        async for session in get_db():
            quiz = await self.get_one(quiz_id)
            if (await actions.validate_user_is_owner(current_user.id, quiz.quiz_company_id, session)
                    or await actions.validate_user_is_admin(current_user.id, quiz.quiz_company_id, session)):
                await session.delete(quiz)
                await session.commit()
                return quiz

    async def get_all_quizzes_in_company(self, company_id: int, page: int, size: int) -> QuizListResponse:
        async for session in get_db():
            offset = (page - 1) * size
            query = select(self.model).where(self.model.quiz_company_id == company_id).offset(offset).limit(size)
            res = await session.execute(query)
            table_name = self.model.__tablename__
            return {table_name: res.scalars().all()}

    async def start_quiz(self, quiz_id, current_user):
        async for session in get_db():
            quiz = await self.get_one(quiz_id)
            questions = await results.get_all_questions_in_quiz(quiz_id, session)
            if not await actions.validate_user_is_member(current_user.id, quiz.quiz_company_id, session):
                raise NotMemberException
            if len(questions) < 2:
                raise NotValidQuizException
            return {"questions": questions}

    async def get_quiz_result(self, quiz_id, body, current_user):
        async for session in get_db():
            quiz = await self.get_one(quiz_id)
            questions = await results.get_all_questions_in_quiz(quiz_id, session)
            result_total_count = len(questions)
            question_correct_answers = await results.calculate_correct_answers(body.model_dump(), questions)

            data = {
                "result_user_id": current_user.id,
                "result_company_id": quiz.quiz_company_id,
                "result_quiz_id": quiz_id,
                "result_right_count": question_correct_answers,
                "result_total_count": result_total_count
            }
            query = insert(Result).values(**data).returning(Result)
            res = await session.execute(query)
            await session.commit()
            return res.scalar_one()