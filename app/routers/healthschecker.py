from fastapi import APIRouter
import redis.asyncio as redisio
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import RedisConfig, DbConfig

router = APIRouter(tags=['healthchecker'])


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


@router.get("/")
async def root():
    response_data = {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }
    return response_data


@router.get("/db_health")
async def check_health():
    postgres_result = await check_postgres_db()
    redis_result = await check_redis()

    if postgres_result["postgres_status"] == "ok" and redis_result["redis_status"] == "ok":
        status_code = 200
        detail = "ok"
        result = "working"
    else:
        status_code = 500
        detail = "Internal Server Error"
        result = "not working"

    response_data = {
        "status_code": status_code,
        "detail": detail,
        "result": result,
        "postgres_result": postgres_result,
        "redis_result": redis_result
    }
    return response_data
