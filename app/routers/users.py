from fastapi import HTTPException, Depends, status, APIRouter, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_connect import get_db
from app.db.models import User
from app.schemas.user_schemas import User as UserModel, UsersListResponse, SignUpRequestModel, UserDetailResponse, UserUpdateRequestModel
from app.repository import users as repository_users
from app.services.auth import auth_service
from app.services.pagination import paginate

router = APIRouter(tags=["users"])


@router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user(body: SignUpRequestModel, db: AsyncSession = Depends(get_db)):
    async with db as session:
        exist_user = await repository_users.get_user_by_email(body.user_email, session)
        if exist_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        body.password = auth_service.get_password_hash(body.password)
        new_user = await repository_users.create_user(body, session)
        return new_user


@router.get("/{user_id}", response_model=UserDetailResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    async with db as session:
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        db_user = result.scalar_one_or_none()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user


@router.put("/{user_id}", response_model=UserDetailResponse)
async def update_user(user_id: int, user: UserUpdateRequestModel, db: AsyncSession = Depends(get_db)):
    async with db as session:
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        db_user = result.scalar_one_or_none()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db_user.password = auth_service.get_password_hash(db_user.password)
        for field, value in user.model_dump().items():
            setattr(db_user, field, value)
        await session.commit()
        await session.refresh(db_user)
        return db_user


@router.delete("/{user_id}", response_model=UserModel)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    async with db as session:
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        db_user = result.scalar_one_or_none()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        await session.delete(db_user)
        await session.commit()
        return db_user


@router.get("/", response_model=UsersListResponse)
async def read_users(
    page: int = Query(1, description="Page number, starting from 1", ge=1),
    size: int = Query(10, description="Number of items per page", le=1000),
    db: AsyncSession = Depends(get_db)
):
    return await paginate(User, page, size, db)
