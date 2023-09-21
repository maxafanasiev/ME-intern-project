
import redis.asyncio as redisio
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import RedisConfig, DbConfig


async def check_postgres_db():
    try:
        db_settings = DbConfig()
        engine = create_async_engine(db_settings.url, echo=True)
        async with engine.connect() as connection:
            await connection.begin()
        return {"postgres_status": "ok"}
    except Exception as e:
        return {"postgres_status": "error", "error_message": str(e)}


async def check_redis():
    try:
        redis_settings = RedisConfig()
        redis = redisio.Redis(host=redis_settings.host, port=redis_settings.port, db=0)
        await redis.ping()
        await redis.close()
        return {"redis_status": "ok"}
    except Exception as e:
        return {"redis_status": "error", "error_message": str(e)}
