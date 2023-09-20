from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_connect import get_db
from app.schemas.user_schemas import User, UsersListResponse, SignUpRequestModel
from app.repository import users as repository_users

router = APIRouter(tags=["users"])


@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(body: SignUpRequestModel, db: AsyncSession = Depends(get_db)):
    async with db as session:
        exist_user = await repository_users.get_user_by_email(body.user_email, session)
        if exist_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        new_user = await repository_users.create_user(body, session)
        return new_user




# # Получение пользователя по ID
# @router.get("/{user_id}", response_model=UserDisplay)
# async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
#     async with db as session:
#         stmt = select(User).where(User.user_id == user_id)
#         result = await session.execute(stmt)
#         db_user = result.scalar_one_or_none()
#         if db_user is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         return db_user
#
# # Обновление пользователя по ID
# @router.put("/{user_id}", response_model=UserDisplay)
# async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
#     async with db as session:
#         stmt = select(User).where(User.user_id == user_id)
#         result = await session.execute(stmt)
#         db_user = result.scalar_one_or_none()
#         if db_user is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         for field, value in user.dict().items():
#             setattr(db_user, field, value)
#         session.commit()
#         session.refresh(db_user)
#         return db_user
#
# # Удаление пользователя по ID
# @router.delete("/{user_id}", response_model=UserDisplay)
# async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
#     async with db as session:
#         stmt = select(User).where(User.user_id == user_id)
#         result = await session.execute(stmt)
#         db_user = result.scalar_one_or_none()
#         if db_user is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         session.delete(db_user)
#         session.commit()
#         return db_user
#
# # Получение списка всех пользователей
# @router.get("/", response_model=List[UserDisplay])
# async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
#     async with db as session:
#         stmt = select(User).offset(skip).limit(limit)
#         result = await session.execute(stmt)
#         return result.scalars().all()
