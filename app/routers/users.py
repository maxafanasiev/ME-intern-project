from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.db.models import User
from app.routers.dependencies import user_service
from app.schemas.validation_schemas import PaginationQueryParams
from app.services.auth_services import auth
from app.services.users import UserService
from app.schemas.user_schemas import User as UserModel, UsersListResponse, UserDetailResponse, UserUpdateRequestModel, \
    SignUpRequestModel

router = APIRouter(tags=["users"])


@router.post("/signup", response_model=UserDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: SignUpRequestModel, user_service: Annotated[UserService, Depends(user_service)]):
    return await user_service.create_user(body)


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user_by_id(user_id: int, user_service: Annotated[UserService, Depends(user_service)]):
    return await user_service.get_user_by_id(user_id)


@router.put("/update", response_model=UserDetailResponse)
async def update_user(user: UserUpdateRequestModel,
                      user_service: Annotated[UserService, Depends(user_service)],
                      current_user: User = Depends(auth.get_current_user)):
    return await user_service.update_user(user, current_user)


@router.delete("/delete", response_model=UserModel)
async def delete_user(user_service: Annotated[UserService, Depends(user_service)],
                      current_user: User = Depends(auth.get_current_user)):
    return await user_service.delete_user(current_user)


@router.get("/", response_model=UsersListResponse)
async def read_users(
        user_service: Annotated[UserService, Depends(user_service)], params: PaginationQueryParams = Depends()
):
    return await user_service.get_all_users(params.page, params.size)
