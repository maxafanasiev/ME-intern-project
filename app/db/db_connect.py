from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import DbConfig

db_settings = DbConfig()

DATABASE_URL = (f"{db_settings.service}://{db_settings.user}:{db_settings.password}"
                f"@{db_settings.domain}:{db_settings.port}/{db_settings.name}")

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncSession(engine) as session:
        yield session

