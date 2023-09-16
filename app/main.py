from fastapi import FastAPI
import uvicorn

from routers import healthschecker
from core.config import settings


app = FastAPI()

app.include_router(healthschecker.router)


if __name__ == "__main__":
    uvicorn.run('main:app', host=settings.host, port=settings.port, reload=settings.reload)
