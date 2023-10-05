from datetime import datetime
from typing import Optional

from sqlalchemy import insert, select

from app.db.db_connect import get_db
from app.db.models import Quiz, User as UserModel
from app.services.action_services import actions
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

    async def get_all_quizzes_in_company(self, company_id, page: int, size: int):
        async for session in get_db():
            offset = (page - 1) * size
            query = select(self.model).where(self.model.quiz_company_id == company_id).offset(offset).limit(size)
            res = await session.execute(query)
            table_name = self.model.__tablename__
            return{table_name: res.scalars().all()}
