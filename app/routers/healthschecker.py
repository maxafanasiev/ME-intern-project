from fastapi import APIRouter, Depends

from app.db.db_connect import get_db

router = APIRouter(tags=['healthchecker'])


@router.get("/")
async def root():
    response_data = {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }
    return response_data


@router.get("/test-postgres/")
async def test_db(db=Depends(get_db)):
    return "postgres work = True" if db else "404"
