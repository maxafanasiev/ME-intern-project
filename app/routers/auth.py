from fastapi import Depends, status, APIRouter, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_connect import get_db
from app.repository import users_repository, auth_repository
from app.schemas.token_schemas import TokenModel
from app.schemas.user_schemas import SignUpRequestModel, UserDetailResponse
from app.services.auth_services import auth_service

router = APIRouter(tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: SignUpRequestModel, db: AsyncSession = Depends(get_db)):
    new_user = await users_repository.create_user(body, db)
    return new_user


@router.post("/signin", response_model=TokenModel)
async def signin(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    access_token, refresh_token, token_type = await auth_repository.login(body, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": token_type}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security),
                        db: AsyncSession = Depends(get_db)):
    access_token, refresh_token, token_type = await auth_repository.refresh_token(credentials, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": token_type}


@router.get("/me", response_model=UserDetailResponse)
async def get_current_user(user: UserDetailResponse = Depends(auth_service.get_current_user)):
    return user
