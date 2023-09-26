from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import insert, select

from app.core.logger import logger
from app.db.db_connect import get_db
from app.db.models import User
from app.services.auth_services import auth_service
from app.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User

    async def add_one(self, data) -> model:
        async for session in get_db():
            exist_user = await auth_service.get_user_by_email(data.user_email, session)
            if exist_user:
                logger.error(f"Error create user")
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
            data.password = await auth_service.get_password_hash(data.password)
            stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def update_one(self, model_id: int, data) -> model:
        async for session in get_db():
            stmt = select(User).where(User.id == model_id)
            result = await session.execute(stmt)
            db_user = result.scalar_one_or_none()
            if db_user is None:
                logger.error(f"Error updating user")
                raise HTTPException(status_code=404, detail="User not found")
            db_user.password = await auth_service.get_password_hash(db_user.password)
            db_user.updated_at = datetime.now()
            for field, value in data.model_dump().items():
                if value is not None:
                    setattr(db_user, field, value)
            await session.commit()
            await session.refresh(db_user)
            return db_user