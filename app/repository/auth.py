from typing import Tuple

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials

from app.core.logger import logger
from app.db.db_connect import get_db
from app.services.auth_services import auth


class AuthRepository:
    async def login(self, body: OAuth2PasswordRequestForm) -> Tuple:
        async for session in get_db():
            user = await auth.get_user_by_email(body.username, session)
            if user is None or not auth.verify_password(body.password, user.password):
                logger.error(f"Login error")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
            access_token = await auth.create_access_token(data={"sub": user.user_email})
            refresh_token = await auth.create_refresh_token(data={"sub": user.user_email})
            await auth.update_token(user, refresh_token, session)
            return access_token, refresh_token, "bearer"

    async def refresh_token(self, credentials: HTTPAuthorizationCredentials) -> Tuple:
        async for session in get_db():
            token = credentials.credentials
            email = await auth.decode_refresh_token(token)
            user = await auth.get_user_by_email(email, session)
            if user.refresh_token != token:
                logger.error(f"Refresh_token error")
                await auth.update_token(user, None, session)
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
            access_token = await auth.create_access_token(data={"sub": email})
            refresh_token = await auth.create_refresh_token(data={"sub": email})
            await auth.update_token(user, refresh_token, session)
            return access_token, refresh_token, "bearer"
