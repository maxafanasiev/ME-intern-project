from typing import Annotated

from fastapi import Depends, status, APIRouter, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.token_schemas import TokenModel
from app.schemas.user_schemas import SignUpRequestModel, UserDetailResponse
from app.services.app_services import app_service
from app.services.auth import AuthService
from app.services.users import UserService
from app.routers.dependencies import user_service, auth_service

router = APIRouter(tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: SignUpRequestModel, user_service: Annotated[UserService, Depends(user_service)]):
    return await user_service.create_user(body)


@router.post("/signin", response_model=TokenModel)
async def signin(auth_service: Annotated[AuthService, Depends(auth_service)],
                 body: OAuth2PasswordRequestForm = Depends()):
    access_token, refresh_token, token_type = await auth_service.login(body)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": token_type}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(auth_service: Annotated[AuthService, Depends(auth_service)],
                        credentials: HTTPAuthorizationCredentials = Security(security)):
    access_token, refresh_token, token_type = await auth_service.refresh_token(credentials)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": token_type}


@router.get("/me", response_model=UserDetailResponse)
async def get_current_user(user=Depends(app_service.get_current_user)):
    return user
