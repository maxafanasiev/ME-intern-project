from fastapi import HTTPException

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.db.models import User


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    async def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    async def get_user_by_email(self, email: str, db: AsyncSession) -> User:
        query = select(User).where(User.user_email == email)
        result = await db.execute(query)
        db_user = result.scalar_one_or_none()
        return db_user

    async def get_user_by_id(self, model_id: int, db: AsyncSession) -> User:
        query = select(User).where(User.id == model_id)
        result = await db.execute(query)
        db_user = result.scalar_one_or_none()
        if db_user is None:
            logger.error(f"Error get user by id")
            raise HTTPException(status_code=404, detail="User not found")
        return db_user


auth_service = Auth()
