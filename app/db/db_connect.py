from sqlalchemy import NullPool
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import DbConfig

db_settings = DbConfig()

engine = create_async_engine(db_settings.url, echo=True)
AsyncDBSession = AsyncSession(engine, expire_on_commit=False, poolclass=NullPool)

Base = declarative_base()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncDBSession as session:
        yield session
