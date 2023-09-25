import redis.asyncio as redisio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import RedisConfig, DbConfig


class PostgresStatusChecker:
    def __init__(self):
        self.db_settings = DbConfig()
        self.engine = create_async_engine(self.db_settings.url, echo=True)

    async def check_status(self):
        try:
            async with self.engine.connect() as connection:
                await connection.begin()
            return True
        except Exception as e:
            return {"postgres_status": "error", "error_message": str(e)}


class RedisStatusChecker:
    def __init__(self):
        self.redis_settings = RedisConfig()

    async def check_status(self):
        try:
            redis = redisio.Redis(host=self.redis_settings.host, port=self.redis_settings.port, db=0)
            await redis.ping()
            return True
        except Exception as e:
            return {"redis_status": "error", "error_message": str(e)}
