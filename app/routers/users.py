from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_connect import get_db
from app.db.models import User
from app.schemas.user_schemas import User as UserModel, UsersListResponse, UserDetailResponse, UserUpdateRequestModel
from app.schemas.validation_schemas import UsersQueryParams
from app.services.auth_services import auth_service
from app.services.pagination import Paginator
from app.repository import users_repository

router = APIRouter(tags=["users"])


@router.get("/{user_id}", response_model=UserDetailResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await users_repository.get_user_by_id(user_id, db)
    return user


@router.put("/", response_model=UserDetailResponse)
async def update_user(user: UserUpdateRequestModel, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    db_user = await users_repository.update_user_by_id(user, db, current_user)
    return db_user


@router.delete("/", response_model=UserModel)
async def delete_user(db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    db_user = await users_repository.delete_user_by_id(db, current_user)
    return db_user


@router.get("/", response_model=UsersListResponse)
async def read_users(params: UsersQueryParams = Depends(),
                     db: AsyncSession = Depends(get_db)
                     ):
    pagination = Paginator(User)
    result = await pagination.paginate(params.page, params.size, db)
    return {"users": result}
