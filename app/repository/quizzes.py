import json
from datetime import datetime
from typing import Optional

from sqlalchemy import insert, select, func

from app.db.db_connect import get_db
from app.db.models import Quiz, User as UserModel, Result
from app.repository.notifications_repo import NotificationRepository as notify
from app.schemas.quiz_schemas import QuizListResponse
from app.services.action_services import actions
from app.services.exceptions import NotMemberException, NotValidQuizException
from app.services.result_services import results
from app.utils.repository import SQLAlchemyRepository
from app.db.redis_utils import redis_db


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
                await self.__send_notifications_to_users_in_company(db_quiz.id, company_id)
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
            if (not await actions.validate_user_is_member(current_user.id, quiz.quiz_company_id, session)
                    and not await actions.validate_user_is_owner(current_user.id, quiz.quiz_company_id, session)):
                raise NotMemberException
            questions = await results.get_all_questions_in_quiz(quiz_id, session)
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
            redis = await redis_db.create_redis_connection()

            quiz_result_key = (f'result:'
                               f'quiz_{quiz_id}:'
                               f'user_{data["result_user_id"]}:'
                               f'company_{data["result_company_id"]}:'
                               f'score_{format(question_correct_answers / result_total_count, ".2f")}')

            await redis_db.set_data(redis, quiz_result_key, json.dumps(data), expire=172800)

            await redis.close()

            query = insert(Result).values(**data).returning(Result)
            res = await session.execute(query)
            await session.commit()
            return res.scalar_one()

    async def __send_notifications_to_users_in_company(self, quiz_id, company_id):
        async for session in get_db():
            members_ids = await actions.get_company_members(company_id, session)
            for member_id in members_ids:
                await notify().create_quiz_notification(member_id, quiz_id, session)

    async def get_last_completion_time(self, user_id, quiz_id, session):
        subquery = select(func.max(Result.created_at).label('max_created_at')).where(
            (Result.result_user_id == user_id) &
            (Result.result_quiz_id == quiz_id)
        ).group_by(Result.result_user_id, Result.result_quiz_id).alias('subquery')

        query = select(subquery.c.max_created_at).order_by(subquery.c.max_created_at.desc()).limit(1)

        result = await session.execute(query)
        last_completion_time = result.scalar()

        return last_completion_time
