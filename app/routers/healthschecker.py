from fastapi import APIRouter
from app.services.healthchecker_funcs import check_redis, check_postgres_db, create_response

router = APIRouter(tags=['healthchecker'])


@router.get("/")
async def root():
    return await create_response(200, "ok", "working")


@router.get("/db_health")
async def check_health():
    postgres_result = await check_postgres_db()

    if postgres_result["postgres_status"] == "ok":
        return await create_response(200, "ok", "working")
    return await create_response(500, "Internal Server Error", "not working")


@router.get("/redis_health")
async def check_health():
    redis_result = await check_redis()

    if redis_result["redis_status"] == "ok":
        return await create_response(200, "ok", "working")
    return await create_response(500, "Internal Server Error", "not working")


