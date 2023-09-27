from typing import Annotated

from fastapi import APIRouter, Query, Depends

from app.routers.dependencies import user_service
from app.services.users import UserService
from app.schemas.user_schemas import User as UserModel, UsersListResponse, UserDetailResponse, UserUpdateRequestModel

router = APIRouter(tags=["users"])


@router.get("/{user_id}", response_model=UserDetailResponse)
async def read_user(user_id: int, user_service: Annotated[UserService, Depends(user_service)]):
    return await user_service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserDetailResponse)
async def update_user(user_id: int, user: UserUpdateRequestModel,
                      user_service: Annotated[UserService, Depends(user_service)]):
    return await user_service.update_user(user_id, user)


@router.delete("/{user_id}", response_model=UserModel)
async def delete_user(user_id: int, user_service: Annotated[UserService, Depends(user_service)]):
    return await user_service.delete_user(user_id)


@router.get("/", response_model=UsersListResponse)
async def read_users(
        user_service: Annotated[UserService, Depends(user_service)],
        page: int = Query(1, description="Page number, starting from 1", ge=1),
        size: int = Query(10, description="Number of items per page", le=1000)
):
    return await user_service.get_all_users(page, size)
