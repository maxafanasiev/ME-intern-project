from fastapi import APIRouter
from app.services.healthchecker_funcs import PostgresStatusChecker, RedisStatusChecker

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
    postgres_checker = PostgresStatusChecker()
    postgres_status_result = await postgres_checker.check_status()

    if postgres_status_result:
        return {
            "status_code": 200,
            "detail": "ok",
            "result": "working"
        }
    return {
        "status_code": 500,
        "detail": "Internal Server Error",
        "result": "not working"
    }


@router.get("/redis_health")
async def check_health():
    redis_checker = RedisStatusChecker()
    redis_status_result = await redis_checker.check_status()

    if redis_status_result:
        return {
            "status_code": 200,
            "detail": "ok",
            "result": "working"
        }

    return {
        "status_code": 500,
        "detail": "Internal Server Error",
        "result": "not working"
    }
