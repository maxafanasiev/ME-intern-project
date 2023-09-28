import string
from datetime import datetime, timedelta
from typing import Optional, Dict
import random

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from starlette import status

from app.core.config import JWTConfig, AUTH0Config
from app.db.db_connect import get_db
from app.core.logger import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.services.exceptions import CredentialException


class Auth:
    jwt_settings = JWTConfig()
    auth0_settings = AUTH0Config()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = jwt_settings.secret_key
    ALGORITHM = jwt_settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

    async def get_user_by_email(self, email: str, db: AsyncSession) -> Optional[User]:
        query = select(User).where(User.user_email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, model_id: int, db: AsyncSession) -> Optional[User]:
        query = select(User).where(User.id == model_id)
        result = await db.execute(query)
        db_user = result.scalar_one_or_none()
        if db_user is None:
            logger.error(f"Error get user by id")
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    async def generate_random_password(self, length=12) -> str:
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    async def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    async def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str) -> Optional[str]:
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    async def decode_and_verify_access_token(self, token: str) -> Optional[Dict]:
        try:
            auth0_decoded = jwt.decode(
                token,
                self.auth0_settings.secret_key,
                algorithms=[self.auth0_settings.algorithm],
                audience=self.auth0_settings.api_audience,
            )
            return auth0_decoded
        except jwt.JWTError:
            pass

        try:
            app_decoded = jwt.decode(
                token,
                self.jwt_settings.secret_key,
                algorithms=[self.jwt_settings.algorithm]
            )
            return app_decoded
        except jwt.JWTError:
            pass

        raise HTTPException(status_code=401, detail="Invalid token")

    async def create_auth0_user(self, email: str, name: str, password: str, db: AsyncSession) -> User:
        try:
            data = {
                "user_email": email,
                "user_firstname": name.split()[0],
                "user_lastname": name.split()[1],
                "password": password
            }
        except Exception as e:
            logger.error(e)
            data = {
                "user_email": email,
                "password": password
            }
        new_user = User(**data)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user


    async def update_token(self, user: User, token: str | None, db: AsyncSession) -> None:
        user.refresh_token = token
        await db.commit()

    async def get_current_user(self, token: str = Depends(oauth2_scheme),
                               db: AsyncSession = Depends(get_db)) -> Optional[User]:
        try:
            payload = await self.decode_and_verify_access_token(token)
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise CredentialException
            elif payload['scope'] == 'openid profile email':
                email = payload["email"]
                if email is None:
                    raise CredentialException
            else:
                raise CredentialException
        except JWTError as e:
            logger.error(e)
            raise CredentialException
        user = await self.get_user_by_email(email, db)
        if user is None and payload['scope'] == 'openid profile email':
            password = await self.get_password_hash(await self.generate_random_password())
            new_user = await self.create_auth0_user(email,
                                                    payload['name'],
                                                    password,
                                                    db)
            return new_user
        if user is None:
            raise CredentialException(detail="Invalid credentials.")
        return user


auth = Auth()
