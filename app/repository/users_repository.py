from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.logger import logger
from app.db.models import User
from app.schemas.user_schemas import SignUpRequestModel
from app.services.auth_services import auth_service
from app.services.users_services import UserServices


async def create_user(body: SignUpRequestModel, db: AsyncSession):
    async with db as session:
        exist_user = await UserServices.get_user_by_email(body.user_email, session)
        if exist_user:
            logger.error(f"Error create user")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        body.password = await auth_service.get_password_hash(body.password)
        new_user = await UserServices.create_user(body, session)
        return new_user


async def get_user_by_id(user_id: int, db: AsyncSession):
    async with db as session:
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        db_user = result.scalar_one_or_none()
        if db_user is None:
            logger.error(f"Error get user by id")
            raise HTTPException(status_code=404, detail="User not found")
        return db_user


def _and(param, param1):
    pass


async def update_user_by_id(user_id: int, update_user, db: AsyncSession, current_user: User):
    async with db as session:
        stmt = select(User).where(_and(User.user_id == user_id, User.user_id == current_user.user_id))
        result = await session.execute(stmt)
        db_user = result.scalar_one_or_none()
        if db_user is None:
            logger.error(f"Error updating user")
            raise HTTPException(status_code=404, detail="User not found")
        db_user.password = await auth_service.get_password_hash(db_user.password)
        db_user.updated_at = datetime.now()
        for field, value in update_user.model_dump().items():
            if value is not None:
                setattr(db_user, field, value)
        await session.commit()
        await session.refresh(db_user)
        return db_user


async def delete_user_by_id(user_id: int, db: AsyncSession, current_user: User):
    async with db as session:
        stmt = select(User).where(_and(User.user_id == user_id, User.user_id == current_user.user_id))
        result = await session.execute(stmt)
        db_user = result.scalar_one_or_none()
        if db_user is None:
            logger.error(f"Error delete user")
            raise HTTPException(status_code=404, detail="User not found")
        await session.delete(db_user)
        await session.commit()
        return db_user
