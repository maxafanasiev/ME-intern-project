from fastapi import APIRouter
from app.services.db_checks import check_redis, check_postgres_db

router = APIRouter(tags=['healthchecker'])


@router.get("/")
async def root():
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }


@router.get("/db_health")
async def check_health():
    postgres_result = await check_postgres_db()

    if postgres_result["postgres_status"] == "ok":
        status_code = 200
        detail = "ok"
        result = "working"
    else:
        status_code = 500
        detail = "Internal Server Error"
        result = "not working"

    return {
        "status_code": status_code,
        "detail": detail,
        "result": result,
        "postgres_result": postgres_result,
    }


@router.get("/redis_health")
async def check_health():
    redis_result = await check_redis()

    if redis_result["redis_status"] == "ok":
        status_code = 200
        detail = "ok"
        result = "working"
    else:
        status_code = 500
        detail = "Internal Server Error"
        result = "not working"

    return {
        "status_code": status_code,
        "detail": detail,
        "result": result,
        "redis_result": redis_result
    }
