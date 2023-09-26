from datetime import datetime

from fastapi import HTTPException, Depends, status, APIRouter, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_connect import get_db
from app.db.models import User
from app.schemas.user_schemas import User as UserModel, UsersListResponse, SignUpRequestModel, UserDetailResponse, \
    UserUpdateRequestModel
from app.services.users_services import UserServices
from app.services.auth_services import auth_service
from app.services.pagination import Paginator
from app.core.logger import logger
from app.repository import users_repository

router = APIRouter(tags=["users"])


@router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user(body: SignUpRequestModel, db: AsyncSession = Depends(get_db)):
    db_user = await users_repository.create_user(body, db)
    return db_user


@router.get("/{user_id}", response_model=UserDetailResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await users_repository.get_user_by_id(user_id, db)
    return user


@router.put("/{user_id}", response_model=UserDetailResponse)
async def update_user(user_id: int, user: UserUpdateRequestModel, db: AsyncSession = Depends(get_db)):
    db_user = await users_repository.update_user_by_id(user_id, user, db)
    return db_user


@router.delete("/{user_id}", response_model=UserModel)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await users_repository.delete_user_by_id(user_id, db)
    return db_user


@router.get("/", response_model=UsersListResponse)
async def read_users(
        page: int = Query(1, description="Page number, starting from 1", ge=1),
        size: int = Query(10, description="Number of items per page", le=1000),
        db: AsyncSession = Depends(get_db)
):
    pagination = Paginator(User)
    result = await pagination.paginate(page, size, db)
    return {"users": result}
