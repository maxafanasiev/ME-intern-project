import redis.asyncio as redisio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import RedisConfig, DbConfig
from app.core.logger import logger


class PostgresStatusChecker:
    def __init__(self):
        self.db_settings = DbConfig()
        self.engine = create_async_engine(self.db_settings.url, echo=True)

    async def check_status(self) -> bool:
        try:
            async with self.engine.connect() as connection:
                await connection.execute(text('SELECT 1'))
            return True
        except Exception as e:
            logger.error(e)
            return False


class RedisStatusChecker:
    def __init__(self):
        self.redis_settings = RedisConfig()

    async def check_status(self) -> bool:
        try:
            redis = redisio.Redis(host=self.redis_settings.host, port=self.redis_settings.port, db=0)
            await redis.ping()
            return True
        except Exception as e:
            logger.error(e)
            return False
