from abc import ABC, abstractmethod
from datetime import datetime

from fastapi import HTTPException
from typing import List, Dict

from sqlalchemy import insert, update, select

from app.core.logger import logger
from app.db.db_connect import get_db


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        raise NotImplementedError

    @abstractmethod
    async def delete_one():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data) -> model:
        async for session in get_db():
            data_dict = dict(data)
            query = insert(self.model).values(**data_dict).returning(self.model)
            res = await session.execute(query)
            await session.commit()
            return res.scalar_one()

    async def get_one(self, model_id: int) -> model:
        async for session in get_db():
            query = select(self.model).where(self.model.id == model_id)
            result = await session.execute(query)
            db_user = result.scalar_one_or_none()
            if db_user is None:
                logger.error(f"Error get entity by id")
                raise HTTPException(status_code=404, detail="Entity not found")
            return db_user

    async def get_all(self, page: int, size: int) -> Dict:
        async for session in get_db():
            offset = (page - 1) * size
            query = select(self.model).offset(offset).limit(size)
            res = await session.execute(query)
            table_name = self.model.__tablename__
            return{table_name: res.scalars().all()}

    async def update_one(self, model_id: int, data: dict) -> model:
        async for session in get_db():
            query = (
                update(self.model)
                .where(self.model.id == model_id)
                .values(**data)
                .returning(self.model)
            )
            res = await session.execute(query)
            res.updated_at = datetime.now()
            await session.commit()
            return res.scalar_one()

    async def delete_one(self, model_id: int) -> model:
        async for session in get_db():
            query = select(self.model).where(self.model.id == model_id)
            result = await session.execute(query)
            db_user = result.scalar_one_or_none()
            if db_user is None:
                logger.error(f"Error delete entity")
                raise HTTPException(status_code=404, detail="Entity not found")
            await session.delete(db_user)
            await session.commit()
            return db_user
