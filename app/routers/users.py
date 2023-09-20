from fastapi import HTTPException, Depends, status, APIRouter, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_connect import get_db
from app.db.models import User
from app.schemas.user_schemas import User as UserModel, UsersListResponse, SignUpRequestModel, UserDetailResponse, \
    UserUpdateRequestModel
from app.repository import users as repository_users
from app.services.auth import auth_service
from app.services.pagination import paginate
from app.core.logger import logger

router = APIRouter(tags=["users"])


@router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user(body: SignUpRequestModel, db: AsyncSession = Depends(get_db)):
    try:
        async with db as session:
            exist_user = await repository_users.get_user_by_email(body.user_email, session)
            if exist_user:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
            body.password = auth_service.get_password_hash(body.password)
            new_user = await repository_users.create_user(body, session)
            return new_user
    except Exception as e:
        logger.error(f"Error create user: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{user_id}", response_model=UserDetailResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        async with db as session:
            stmt = select(User).where(User.user_id == user_id)
            result = await session.execute(stmt)
            db_user = result.scalar_one_or_none()
            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return db_user
    except Exception as e:
        logger.error(f"Error get user by id: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.put("/{user_id}", response_model=UserDetailResponse)
async def update_user(user_id: int, user: UserUpdateRequestModel, db: AsyncSession = Depends(get_db)):
    try:
        async with db as session:
            stmt = select(User).where(User.user_id == user_id)
            result = await session.execute(stmt)
            db_user = result.scalar_one_or_none()
            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            db_user.password = auth_service.get_password_hash(db_user.password)
            for field, value in user.model_dump().items():
                if value is not None:
                    setattr(db_user, field, value)
            await session.commit()
            await session.refresh(db_user)
            return db_user
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/{user_id}", response_model=UserModel)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        async with db as session:
            stmt = select(User).where(User.user_id == user_id)
            result = await session.execute(stmt)
            db_user = result.scalar_one_or_none()
            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            await session.delete(db_user)
            await session.commit()
            return db_user
    except Exception as e:
        logger.error(f"Error delete user: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/", response_model=UsersListResponse)
async def read_users(
        page: int = Query(1, description="Page number, starting from 1", ge=1),
        size: int = Query(10, description="Number of items per page", le=1000),
        db: AsyncSession = Depends(get_db)
):
    try:
        result = await paginate(User, page, size, db)
        user_list = [
            UserModel(
                user_id=user.user_id,
                user_email=user.user_email,
                user_firstname=user.user_firstname,
                user_lastname=user.user_lastname,
            )
            for user in result
        ]
        print(user_list)
        return {"users": user_list}
    except Exception as e:
        logger.error(f"Error get users: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
