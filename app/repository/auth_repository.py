from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.logger import logger
from app.services.auth_services import auth_service
from app.services.users_services import UserServices


async def login(body: OAuth2PasswordRequestForm, db: AsyncSession):
    async with db as session:
        user = await UserServices.get_user_by_email(body.username, session)
        if user is None or not auth_service.verify_password(body.password, user.password):
            logger.error(f"Login error")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        access_token = await auth_service.create_access_token(data={"sub": user.user_email})
        refresh_token = await auth_service.create_refresh_token(data={"sub": user.user_email})
        await UserServices.update_token(user, refresh_token, session)
        return access_token, refresh_token, "bearer"


async def refresh_token(credentials: HTTPAuthorizationCredentials,
                        db: AsyncSession):
    async with db as session:
        token = credentials.credentials
        email = await auth_service.decode_refresh_token(token)
        user = await UserServices.get_user_by_email(email, session)
        if user.refresh_token != token:
            logger.error(f"Refresh_token error")
            await UserServices.update_token(user, None, session)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        access_token = await auth_service.create_access_token(data={"sub": email})
        refresh_token = await auth_service.create_refresh_token(data={"sub": email})
        await UserServices.update_token(user, refresh_token, session)
        return access_token, refresh_token, "bearer"