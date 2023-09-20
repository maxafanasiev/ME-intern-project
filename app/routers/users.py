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
