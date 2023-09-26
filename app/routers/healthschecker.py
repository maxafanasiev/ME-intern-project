from fastapi import APIRouter, Depends, HTTPException
from app.services.healthchecker_services import PostgresStatusChecker, RedisStatusChecker

router = APIRouter(tags=['healthchecker'])


@router.get("/")
async def root():
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }


@router.get("/db_health")
async def check_health(postgres_checker: PostgresStatusChecker = Depends(PostgresStatusChecker)):
    postgres_status_result = await postgres_checker.check_status()

    if postgres_status_result:
        return {
            "status_code": 200,
            "detail": "ok",
            "result": "working"
        }
    raise HTTPException(status_code=500, detail="Postgres Connection Error")


@router.get("/redis_health")
async def check_health(redis_checker: RedisStatusChecker = Depends(RedisStatusChecker)):
    redis_status_result = await redis_checker.check_status()

    if redis_status_result is True:
        return {
            "status_code": 200,
            "detail": "ok",
            "result": "working"
        }

    raise HTTPException(status_code=500, detail="Redis Connection Error")
