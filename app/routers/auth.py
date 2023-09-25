from fastapi import HTTPException, Depends, status, APIRouter, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_connect import get_db
from app.schemas.token_schemas import TokenModel
from app.schemas.user_schemas import SignUpRequestModel, UserDetailResponse
from app.services.users_services import UserServices
from app.services.auth_services import auth_service
from app.core.logger import logger

router = APIRouter(tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: SignUpRequestModel, db: AsyncSession = Depends(get_db)):
    try:
        async with db as session:
            exist_user = await UserServices.get_user_by_email(body.user_email, session)
            if exist_user:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
            body.password = auth_service.get_password_hash(body.password)
            new_user = await UserServices.create_user(body, session)
            return new_user
    except Exception as e:
        logger.error(f"Error create user: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/signin", response_model=TokenModel)
async def signin(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    try:
        async with db as session:
            user = await UserServices.get_user_by_email(body.username, session)
            if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
            if not auth_service.verify_password(body.password, user.password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
            access_token = await auth_service.create_access_token(data={"sub": user.user_email})
            refresh_token = await auth_service.create_refresh_token(data={"sub": user.user_email})
            await UserServices.update_token(user, refresh_token, session)
            return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security),
                        db: AsyncSession = Depends(get_db)):
    try:
        async with db as session:
            token = credentials.credentials
            email = await auth_service.decode_refresh_token(token)
            user = await UserServices.get_user_by_email(email, session)
            if user.refresh_token != token:
                await UserServices.update_token(user, None, session)
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

            access_token = await auth_service.create_access_token(data={"sub": email})
            refresh_token = await auth_service.create_refresh_token(data={"sub": email})
            await UserServices.update_token(user, refresh_token, session)
            return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Refresh_token error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/me", response_model=UserDetailResponse)
async def get_current_user(user: UserDetailResponse = Depends(auth_service.get_current_user)):
    return user
