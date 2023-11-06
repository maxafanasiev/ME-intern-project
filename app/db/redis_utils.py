import redis.asyncio as aioredis

from app.core.config import RedisConfig


class RedisDB:
    redis_settings = RedisConfig()

    async def create_redis_connection(self):
        return await aioredis.Redis(host=self.redis_settings.host, port=self.redis_settings.port, db=0)

    async def set_data(self, redis, key, value, expire=None):
        await redis.set(key, value)
        await redis.expire(key, expire)

    async def get_data(self, redis, key):
        return await redis.get(key)


redis_db = RedisDB()
