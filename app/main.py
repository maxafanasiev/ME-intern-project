import uvicorn
import redis.asyncio as redisio
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.backends.redis import RedisBackend

from routers import healthschecker
from app.core.config import FastAPIConfig, RedisConfig, origins

fastapi_settings = FastAPIConfig()
redis_settings = RedisConfig()

app = FastAPI()
redis = redisio.Redis(host=redis_settings.host, port=redis_settings.port, db=0)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthschecker.router)


@app.on_event("startup")
async def startup_event():
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


@app.on_event("shutdown")
async def shutdown_event():
    await redis.close()


if __name__ == "__main__":
    uvicorn.run('main:app', host=fastapi_settings.host, port=fastapi_settings.port, reload=fastapi_settings.reload)
