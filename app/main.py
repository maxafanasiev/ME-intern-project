import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.backends.redis import RedisBackend

from app.routers import healthschecker, users, auth, companies, company_actions, user_actions, quizzes, questions, \
    scores
from app.core.config import FastAPIConfig, RedisConfig, origins
from app.core.logger import logger
from app.db.redis_utils import redis_db

fastapi_settings = FastAPIConfig()
redis_settings = RedisConfig()

app = FastAPI()
redis_connection = None

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
app.include_router(company_actions.router, prefix='/company-actions')
app.include_router(user_actions.router, prefix='/user-actions')
app.include_router(quizzes.router, prefix='/quizzes')
app.include_router(questions.router, prefix='/questions')
app.include_router(scores.router, prefix='/scores')


@app.on_event("startup")
async def startup_event():
    logger.info("App started")
    global redis_connection
    redis_connection = await redis_db.create_redis_connection()
    FastAPICache.init(RedisBackend(redis_connection), prefix='app-cache')


@app.on_event("shutdown")
async def shutdown_event():
    await redis_connection.close()


if __name__ == "__main__":
    uvicorn.run('main:app', host=fastapi_settings.host, port=fastapi_settings.port, reload=fastapi_settings.reload)
