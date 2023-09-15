from fastapi import FastAPI
import uvicorn

from routers import healthschecker


app = FastAPI()

app.include_router(healthschecker.router)


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
