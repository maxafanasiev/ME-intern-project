from typing import Annotated

from fastapi import APIRouter, Query, Depends

from app.db.models import User
from app.routers.dependencies import user_service
from app.services.app_services import app_service
from app.services.users import UserService
from app.schemas.user_schemas import User as UserModel, UsersListResponse, UserDetailResponse, UserUpdateRequestModel
from app.schemas.validation_schemas import PaginationQueryParams

router = APIRouter(tags=["users"])


@router.get("/{user_id}", response_model=UserDetailResponse)
async def read_user(user_id: int, user_service: Annotated[UserService, Depends(user_service)]):
    return await user_service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserDetailResponse)
async def update_user(user_id: int, user: UserUpdateRequestModel,
                      user_service: Annotated[UserService, Depends(user_service)],
                      current_user: User = Depends(app_service.get_current_user)):
    return await user_service.update_user(user_id, user, current_user)


@router.delete("/{user_id}", response_model=UserModel)
async def delete_user(user_id: int, user_service: Annotated[UserService, Depends(user_service)],
                      current_user: User = Depends(app_service.get_current_user)):
    return await user_service.delete_user(user_id, current_user)


@router.get("/", response_model=UsersListResponse)
async def read_users(
        user_service: Annotated[UserService, Depends(user_service)], params: PaginationQueryParams = Depends()
):
    return {"users": await user_service.get_all_users(params.page, params.size)}
