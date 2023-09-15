from fastapi import APIRouter

router = APIRouter(tags=['healthchecker'])


@router.get("/")
async def root():
    response_data = {"status_code": 200,
                     "detail": "ok",
                     "result": "working",
                     }
    return response_data
