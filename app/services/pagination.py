from sqlalchemy import select
from typing import Type

from fastapi import Query, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_connect import get_db


class Paginator:
    def __init__(self, entity: Type[BaseModel]):
        self.entity = entity

    async def paginate(
            self,
            page: int = Query(1, description="Page number, starting from 1", ge=1),
            size: int = Query(100, description="Number of items per page", le=1000),
            db: AsyncSession = Depends(get_db)
    ):
        async with db as session:
            offset = (page - 1) * size
            stmt = select(self.entity).offset(offset).limit(size)
            result = await session.execute(stmt)
            return result.scalars().all()
