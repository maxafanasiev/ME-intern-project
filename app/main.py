import uvicorn
import redis.asyncio as redisio
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.backends.redis import RedisBackend

from app.db.db_connect import init_models
from app.routers import healthschecker, users, auth, companies, company_actions, user_actions
from app.core.config import FastAPIConfig, RedisConfig, origins
from app.core.logger import logger

fastapi_settings = FastAPIConfig()
redis_settings = RedisConfig()

redis = redisio.Redis(host=redis_settings.host, port=redis_settings.port, db=0)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthschecker.router)
app.include_router(users.router, prefix='/users')
app.include_router(auth.router, prefix='/auth')
app.include_router(companies.router, prefix='/companies')
app.include_router(company_actions.router, prefix='/company_actions')
app.include_router(user_actions.router, prefix='/user_actions')


@app.on_event("startup")
async def startup_event():
    logger.info("App started")
    FastAPICache.init(RedisBackend(redis), prefix='app-cache')


@app.on_event("shutdown")
async def shutdown_event():
    await redis.close()


if __name__ == "__main__":
    uvicorn.run('main:app', host=fastapi_settings.host, port=fastapi_settings.port, reload=fastapi_settings.reload)
