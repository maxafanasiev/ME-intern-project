from libgravatar import Gravatar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schemas.user_schemas import SignUpRequestModel


class UserServices:
    @staticmethod
    async def get_user_by_email(email: str, db: AsyncSession) -> User:
        stmt = select(User).where(User.user_email == email)
        result = await db.execute(stmt)
        db_user = result.scalar_one_or_none()
        return db_user

    @staticmethod
    async def create_user(body: SignUpRequestModel, db: AsyncSession) -> User:
        if body.user_avatar is None:
            try:
                g = Gravatar(body.user_email)
                avatar = g.get_image()
                body.user_avatar = avatar
            except Exception as e:
                print(e)
        new_user = User(**body.model_dump())
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
        user.refresh_token = token
        await db.commit()
