import os

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    response_data = {"status_code": 200,
                     "detail": "ok",
                     "result": "working",
                     }
    return response_data


if __name__ == "__main__":
    os.system("uvicorn app.main:app --reload")
